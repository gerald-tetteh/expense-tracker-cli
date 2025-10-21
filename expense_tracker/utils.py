import locale
import platform


class Utils:
    """Utility functions for the expense tracker application."""
    monthOrdinals = {
        "Jan": "1",
        "Feb": "2",
        "Mar": "3",
        "Apr": "4",
        "May": "5",
        "Jun": "6",
        "Jul": "7",
        "Aug": "8",
        "Sep": "9",
        "Oct": "10",
        "Nov": "11",
        "Dec": "12"
    }

    @staticmethod
    def format_currency(amount: float) -> str:
        """
        Format a number as a currency string.

        Args:
            amount (float): The amount to format.
        """
        try:
            loc = locale.getlocale()
            if loc == (None, None):
                if platform.system() == "Windows":
                    locale.setlocale(
                        locale.LC_ALL, "English_United States.1252")
                else:
                    locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
        except Exception:
            if platform.system() == "Windows":
                locale.setlocale(locale.LC_ALL, "English_United States.1252")
            else:
                locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
        try:
            return locale.currency(amount, grouping=True)
        except Exception:
            return f"${amount:,.2f}"

    @staticmethod
    def month_text_to_ordinal(month: str) -> str:
        """
        Returns the ordinal for the months of the year.
        Eg: Jan = 1, Feb = 2.

        Args:
            month (str): Short form of the month
        """
        if month not in Utils.monthOrdinals:
            raise ValueError(
                f"Invalid month. Available options: {", ".join(Utils.monthOrdinals.keys())}")
        return Utils.monthOrdinals[month]
