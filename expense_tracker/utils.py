import locale
import platform


class Utils:
    """Utility functions for the expense tracker application."""

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
