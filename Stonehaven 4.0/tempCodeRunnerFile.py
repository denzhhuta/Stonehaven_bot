@dp.message_handler(state="online_check")
async def input_name(message: types.Message, state: FSMContext):
    player_name = message.text
    ip_address = "193.169.195.76" 
    port = 25565
    await state.update_data(player_name=player_name)
    await state.reset_state()
    
    message_text = await check_online(ip_address, port, player_name)
    await bot.send_message(chat_id=message.from_user.id,
                           text=message_text,
                           parse_mode="HTML")