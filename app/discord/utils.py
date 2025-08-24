from typing import Optional

from loguru import logger


async def send_long_message(channel, message: str, max_length: int = 2000) -> Optional[object]:
    try:
        if not message or not message.strip():
            logger.debug("Empty message received, skipping send")
            return

        logger.debug(f"Processing message of length: {len(message)}")
        if len(message) <= max_length:
            sent_message = await channel.send(message)
            logger.debug("Message sent directly (under character limit)")
            return sent_message

        chunks = []
        lines = message.split("\n")
        current_chunk = ""
        in_code_block = False
        code_block_lang = ""

        i = 0
        while i < len(lines):
            line = lines[i]

            if line.strip().startswith("```"):
                if not in_code_block:
                    in_code_block = True
                    code_block_lang = line.strip()[3:].strip()

                    if current_chunk and len(current_chunk) + len(line) + 1 > max_length:
                        chunks.append(current_chunk.rstrip())
                        current_chunk = ""

                    current_chunk += line + "\n"
                else:
                    current_chunk += line + "\n"
                    in_code_block = False

                    if len(current_chunk) > max_length * 0.8:
                        chunks.append(current_chunk.rstrip())
                        current_chunk = ""

            elif in_code_block:
                if len(current_chunk) + len(line) + 1 > max_length:
                    current_chunk += "```\n"
                    chunks.append(current_chunk.rstrip())

                    lang_marker = f"```{code_block_lang}" if code_block_lang else "```"
                    current_chunk = lang_marker + "\n" + line + "\n"
                else:
                    current_chunk += line + "\n"

            else:
                if len(line) > max_length:
                    if current_chunk.strip():
                        chunks.append(current_chunk.rstrip())
                        current_chunk = ""

                    words = line.split(" ")
                    temp_line = ""

                    for word in words:
                        if len(temp_line) + len(word) + 1 <= max_length:
                            temp_line += (" " if temp_line else "") + word
                        else:
                            if temp_line:
                                chunks.append(temp_line)
                                temp_line = word
                            else:
                                chunks.append(word[:max_length])
                                temp_line = word[max_length:]

                    if temp_line:
                        current_chunk = temp_line + "\n"

                elif len(current_chunk) + len(line) + 1 <= max_length:
                    current_chunk += line + "\n"
                else:
                    if current_chunk.strip():
                        chunks.append(current_chunk.rstrip())
                    current_chunk = line + "\n"

            i += 1

        if current_chunk.strip():
            if in_code_block and not current_chunk.rstrip().endswith("```"):
                current_chunk += "```"
            chunks.append(current_chunk.rstrip())

        logger.debug(f"Sending message in {len(chunks)} chunks")
        last_message = None
        for i, chunk in enumerate(chunks):
            if chunk.strip():
                logger.debug(f"Sending chunk {i + 1}/{len(chunks)} (length: {len(chunk)})")
                last_message = await channel.send(chunk)
            else:
                logger.debug(f"Skipping empty chunk {i + 1}")
        return last_message

    except Exception as e:
        logger.error(f"Error in send_long_message: {e}")
        try:
            logger.warning("Attempting fallback: sending truncated message")
            return await channel.send(message[:max_length])
        except Exception as fallback_error:
            logger.error(f"Fallback send failed: {fallback_error}")
            return await channel.send("Sorry, I encountered an error sending my response.")
