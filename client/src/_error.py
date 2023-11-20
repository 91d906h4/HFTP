def error(code: str, message: str="", end: bool=True) -> None:
    codes = {
        "001": "Welcome message miss.",
    }

    if code in codes: title = codes[code]
    else: title = "Unknown error."

    print(f"Code: {code}\n \
            Title: {title}\n \
            Message: {message}"
        )

    if end: exit(-1)