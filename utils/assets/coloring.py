import os
import sty


class Coloring:
    """ Class for coloring and formatting text. """

    white = 0xFFFFFF
    red = 0xef4a4a
    green = 0x4aef4f
    blue = 0x5865F2

    Text = sty.fg
    Back = sty.bg
    Form = sty.ef
    Rest = sty.rs


    @staticmethod
    def init() -> None:
        """ Runs a system call to enable colors and formats in the console. """

        os.system('')


    @staticmethod
    def _gradient1d(input_str: str, start: tuple[int, int, int], end: tuple[int, int, int]) -> str:
        """ Helper function for creating 1D gradients. """

        steps = len(input_str)
        r_step = (end[0] - start[0]) / (steps - 1)
        g_step = (end[1] - start[1]) / (steps - 1)
        b_step = (end[2] - start[2]) / (steps - 1)

        output_str = ''
        for i, char in enumerate(input_str):
            r = int(start[0] + r_step * i)
            g = int(start[1] + g_step * i)
            b = int(start[2] + b_step * i)

            output_str += f'{Coloring.Text(r, g, b)}{char}'

        return output_str + Coloring.Text.rs


    @staticmethod
    def _gradient2d(lines: list[str], start: tuple[int, int, int], end: tuple[int, int, int]) -> str:
        """ Helper function for creating 2D gradients. """

        total_chars = sum(len(line) for line in lines)
        r_step = (end[0] - start[0]) / total_chars
        g_step = (end[1] - start[1]) / total_chars
        b_step = (end[2] - start[2]) / total_chars

        output_str = ''
        char_count = 0

        for line in lines:
            for char in line:
                r = int(start[0] + r_step * char_count)
                g = int(start[1] + g_step * char_count)
                b = int(start[2] + b_step * char_count)

                output_str += f'{Coloring.Text(r, g, b)}{char}'
                char_count += 1

            output_str += '\n'

        return output_str + Coloring.Text.rs


    @staticmethod
    def gradient(input_str: str, start: tuple[int, int, int], end: tuple[int, int, int]) -> str:
        """
        Color a string into a gradient.

        Arguments:
             input_str: The original string.
             start: The rgb value from which the gradient starts.
             end: The rgb value at which the gradient ends.

        Returns:
            The colored string.
        """

        if not input_str or len(input_str) < 2:
            return ''

        lines = input_str.split('\n')
        if len(lines) == 1:
            return Coloring._gradient1d(input_str, start, end)

        return Coloring._gradient2d(lines, start, end)


__all__ = ['Coloring']
