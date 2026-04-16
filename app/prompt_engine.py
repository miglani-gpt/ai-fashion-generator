def refine_prompt(prev_prompt, user_input):
    base_style = "high fashion, detailed, professional, runway, 4k"

    if prev_prompt == "":
        return user_input + ", " + base_style

    return prev_prompt + ", " + user_input