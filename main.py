import os
if len(args) < 2 or args[1].strip().lower() not in ('white', 'black'):
await m.reply_text('Usage: /setcolor white OR /setcolor black')
return
USER_SETTINGS[user.id] = USER_SETTINGS.get(user.id, {})
USER_SETTINGS[user.id]['color'] = args[1].strip().lower()
await m.reply_text(f"Watermark color set to: {args[1].strip().lower()}")




@app.on_message(filters.command('setsize') & filters.private)
async def set_size(c: Client, m: Message):
user = m.from_user
if not user:
return
args = m.text.split(' ', 1)
if len(args) < 2:
await m.reply_text('Usage: /setsize 24')
return
try:
size = int(args[1].strip())
if size < 10 or size > 200:
raise ValueError()
except Exception:
await m.reply_text('Size must be a number between 10 and 200')
return
USER_SETTINGS[user.id] = USER_SETTINGS.get(user.id, {})
USER_SETTINGS[user.id]['size'] = size
await m.reply_text(f"Watermark font size set to: {size}")




@app.on_message(filters.video & filters.private)
async def handle_video(c: Client, m: Message):
user = m.from_user
if not user:
return
msg = await m.reply_text('Downloading video...')
settings = get_settings(user.id)


input_path = f"/tmp/input_{uuid.uuid4().hex}.mp4"
output_path = f"/tmp/output_{uuid.uuid4().hex}.mp4"


try:
await m.download(file_name=input_path)
await msg.edit('Applying watermark...')
await add_centered_text_watermark(input_path, output_path, settings['text'], settings['color'], settings['size'])
await msg.edit('Uploading watermarked video...')
await c.send_video(chat_id=m.chat.id, video=output_path, caption='Here is your watermarked video')
await msg.delete()
except Exception as e:
await msg.edit(f'Error: {e}')
finally:
for p in (input_path, output_path):
try:
os.remove(p)
except Exception:
pass




if __name__ == '__main__':
app.run()
