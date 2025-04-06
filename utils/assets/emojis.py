import random
import pyemojify


class Emoji:
    """ Class for using emojis. """

    cat_bongo = '<a:bongo:886287312881864714>'
    cat_bonk = '<a:catbonk:1096384738052284437>'
    cat_finger = '<:catFinger:1241723204683174009>'
    cat_punch = '<:boks:1283457579032379442>'
    qwan = '<:qwan:1230195770053886094>'

    enola = '<:ee:1286292044460986441>'
    blank = '<:ee:1105122910051508225>'

    check = '<:ee:1105122920159772784>'
    denied = '<:ee:1105122927554338960>'
    error = '<:ee:1105122928892334111>'
    warning = '<:ee:1105509639778467883>'
    info = '<:ee:1105509087896146071>'
    question = '<:ee:1105122980759081030>'
    slash = '<:ee:1105509426909171833>'
    reply = '<:ee:1311075281733423166>'

    bar_str_empty = '<:ee:1106587508596285552>'
    bar_str_half = '<:ee:1106587505798693025>'
    bar_str_full = '<:ee:1106587503546347630>'
    bar_mid_empty = '<:ee:1106587500983635968>'
    bar_mid_half = '<:ee:1106587499540783244>'
    bar_mid_full = '<:ee:1106587497284243579>'
    bar_end_empty = '<:ee:1106587496055324682>'
    bar_end_half = '<:ee:1106587494700548126>'
    bar_end_full = '<:ee:1106587491777126461>'

    ping_good = '<:ee:1105122977206517890>'
    ping_ok = '<:ee:1105509430415597649>'
    ping_bad = '<:ee:1105509319719534682>'

    language = '<:ee:1105122942746112151>'
    delete = '<:ee:1105509041964327003>'
    archive = '<:ee:1105508991620087869>'
    bookmark = '<:ee:1105508994883264524>'
    calendar = '<:ee:1105508996418375713>'
    channel = '<:ee:1105508999136288808>'
    chat = '<:ee:1105509000667201656>'
    time = '<:ee:1105509039443562577>'
    folder = '<:ee:1105509043444912208>'
    game = '<:ee:1105509044485107814>'
    globe = '<:ee:1105509047140102215>'
    heart = '<:ee:1105509080145068183>'
    home = '<:ee:1105509083072712867>'
    id = '<:ee:1105509085144682576>'
    link = '<:ee:1105509089129283634>'
    megaphone = '<:ee:1105509310995374182>'
    message = '<:ee:1105509314094956565>'
    note = '<:ee:1105509315651055698>'
    pen = '<:ee:1105509318247325736>'
    lock = '<:ee:1105509322571653251>'
    settings = '<:ee:1105509424140918815>'
    shield = '<:ee:1105509425478909982>'
    reload = '<:ee:1105509421494313090>'
    speech = '<:ee:1106243083680624771>'
    tv = '<:ee:1105509541518516415>'
    upload = '<:ee:1105509544265797782>'
    stats = '<:ee:1106243081344393267>'
    ticket = '<:ee:1105509554323734569>'
    trashcan = '<:ee:1105509564809490614>'
    user = '<:ee:1105509635408019527>'
    wave = '<:ee:1105509641942749285>'

    thumbsup = '<:ee:1105122994587697172>'
    thumbsdown = '<:ee:1105509548460089395>'

    circle_green = '<:ee:1118168053453176952>'
    circle_yellow = '<:ee:1118168057681039370>'
    circle_red = '<:ee:1118168055768436879>'
    circle_blue = '<:ee:1247260406565834793>'

    emojify = pyemojify.emojify


    class unicode:
        """ Subclass for unicode emojis. """

        reply = '⤷'


    class loading:
        """ Subclass for loading emojis. """

        circle = '<a:ae:1105122946063794246>'
        discord = '<a:ae:1105122951172464783>'
        discord_logo = '<a:ae:1105122955849121842>'
        dots = '<a:ae:1105122958151786648>'
        dots_fancy = '<a:ae:1105122960068579368>'
        line = '<a:ae:1105122964137054269>'
        line_fancy = '<a:ae:1105509130208297091>'
        gears = '<a:ae:1105509236953317527>'

        def __init__(self) -> None:
            """ Create a list of all the loading emojis. """

            self.emojis = [
                attr for attr in vars(self.__class__).keys()
                if not attr.startswith('__')
            ]

        @staticmethod
        def random() -> str:
            """ Get a random loading emoji. """

            return getattr(Emoji.loading, random.choice(Emoji.loading().emojis))


__all__ = ['Emoji']
