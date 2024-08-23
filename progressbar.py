"""Module for functions to print progress bar to the console"""


def progress_bar(
    iterable, prefix="", suffix="", decimals=1, length=100, fill="█", print_end="\r"
):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        print_end   - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    total = len(iterable)
    # Progress Bar Printing Function

    def print_progress_bar(iteration):
        """print progress bar in the console

        Args:
            iteration (_type_): _description_
        """
        percent = ("{0:." + str(decimals) + "f}").format(
            100 * (iteration / float(total))
        )
        filled_length = int(length * iteration // total)
        progress_line = fill * filled_length + "-" * (length - filled_length)
        iteration_str = str(iteration).zfill(len(str(total)))
        progress_message = f"\r{prefix} ({iteration_str}/{total}) |{progress_line}| {percent}% {suffix}"
        print(
            progress_message,
            end=print_end,
        )

    # Initial Call
    print_progress_bar(0)
    # Update Progress Bar
    for i, item in enumerate(iterable):
        yield item
        print_progress_bar(i + 1)
    # Print New Line on Complete
    print()
