import asyncio
import shlex
import os
import uuid
import subprocess


async def run_ffmpeg(cmd: str):
# Run ffmpeg asynchronously using a thread-safe subprocess call
proc = await asyncio.create_subprocess_shell(
cmd,
stdout=asyncio.subprocess.PIPE,
stderr=asyncio.subprocess.PIPE,
)
out, err = await proc.communicate()
return proc.returncode, out, err




def escape_text(txt: str) -> str:
# basic escaping for drawtext; avoid single quotes and colons
return txt.replace("\\", "\\\\").replace("'", "\\'")


async def add_centered_text_watermark(input_path: str, output_path: str, text: str, color: str = 'white', fontsize: int = 36):
"""
Uses ffmpeg drawtext to overlay centered text.
- color: 'white' or 'black'
- fontsize: integer (approx px)
"""
fontfile = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
if not os.path.exists(fontfile):
# fallback: no font specified, let ffmpeg pick default
fontfile_param = ""
else:
fontfile_param = f":fontfile={fontfile}"


safe_text = escape_text(text)


# drawtext: x and y calculate center dynamically using text_w/text_h
drawtext = (
"drawtext=text='{}':x=(w-text_w)/2:y=(h-text_h)/2:fontcolor={}:fontsize={}:box=1:boxcolor=black@0.0{}"
.format(safe_text, color, fontsize, fontfile_param)
)


# build command
# keep original codecs when possible; transcode only if needed
cmd = (
f"ffmpeg -y -i {shlex.quote(input_path)} -vf \"{drawtext}\" -c:v libx264 -preset veryfast -crf 20 -c:a copy {shlex.quote(output_path)}"
)


returncode, out, err = await run_ffmpeg(cmd)
if returncode != 0:
raise RuntimeError(f"ffmpeg failed: {err.decode(errors='ignore')}\ncmd: {cmd}")
return output_path
