from discord import Embed, Color

"""
Functions for creating basic embeds
"""

def simpleEmbed(title, text, color=Color.blue()):
    return Embed(description=text, title=title, color=color)