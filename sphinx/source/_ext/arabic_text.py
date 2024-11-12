import re
from sphinx.transforms import SphinxTransform
from docutils import nodes

class SubsTextTransform(SphinxTransform):
    """Base classe that Defines a Transform that substitues latin characters 
    by unicode characters"""

    default_priority = 500  # Runs at a typical priority level

    # The pattern that matches the command 
    pattern = re.compile(r'command\|\[(.*?)\]')

    # Matching dictionnary
    matching_dict_priority_0 = {}
    matching_dict_priority_1 = {}

    def apply(self):
        # Iterate over all text nodes in the document
        for node in self.document.traverse(nodes.Text):
            
            # Placeholders 
            buffer_text = None
            buffer_text_2 = node.astext()

            # Iterate until no change is made
            while (buffer_text != buffer_text_2):

                buffer_text = buffer_text_2

                # Replaces the text if applicable
                buffer_text_2 = self.replace_command(
                    command_pattern=self.pattern, 
                    text=buffer_text,
                )
            
            # Replace in the build
            if buffer_text != node.astext():
                node.parent.replace(node, nodes.Text(buffer_text))

    def replace_command(
            self, 
            command_pattern:re.Pattern[str], 
            text:str,
        )->str:
        """Replaces character by character

        Args:
            command_pattern (re.Pattern[str]): The regex that matches the command
            text (str): The text to be modified

        Returns:
            str: The result
        """

        matched = command_pattern.search(text)
        if matched :
            text_to_subs = matched.group(1)
            for initial_char, new_char in self.matching_dict_priority_0.items():
                text_to_subs = text_to_subs.replace(initial_char, new_char)
            for initial_char, new_char in self.matching_dict_priority_1.items():
                text_to_subs = text_to_subs.replace(initial_char, new_char)
            return text.replace(matched.group(), text_to_subs)
        return text

class ArabSubs(SubsTextTransform):
    """Defines a Transform that substitues latin characters by arab ones"""

    # The pattern that matches the command 
    pattern = re.compile(r'arab\|\[(.*?)\]')

    # Matching dictionnary
    matching_dict_priority_0 = {
        "<th>" : "ث",
        "<TH>" : "ث",
        "<hb>" : "ح",
        "<HB>" : "ح",
        "<dh>" : "ذ",
        "<DH>" : "ذ",
        "<vs>" : "ش",
        "<VS>" : "ش",
        "<cs>" : "ص",
        "<CS>" : "ص",
        "<cdh>" : "ض",
        "<CDH>" : "ض",
        "<ct>" : "ط",
        "<CT>" : "ط",
        "<cdh2>" : "ظ",
        "<CDH2>" : "ظ",
        "<ca>" : "ع",
        "<CA>" : "ع",
        "<vr>" : "غ",
        "<VR>" : "غ",
        "<A>" : "أ",
        "<I>" : "إ",
        "<->" : "ء",
        "<W>" : "ؤ",
        "<O>" : "ئ",
        "<Y>" : "ى",
        "<tt>" : "ة",
        "<~>" : "ّ",
        "<va>" : "ً",
        "<vo>" : "ٌ",
        "<vi>" : "ٍ",
    }
    matching_dict_priority_1 = {
        "b" : "ب",
        "B" : "ب",
        "t" : "ت",
        "T" : "ت",
        "j" : "ج",
        "J" : "ج",
        "x" : "خ",
        "X" : "خ",
        "d" : "د",
        "D" : "د",
        "r" : "ر",
        "R" : "ر",
        "z" : "ز",
        "Z" : "ز",
        "s" : "س",
        "S" : "س",
        "f" : "ف",
        "F" : "ف",
        "q" : "ق",
        "Q" : "ق",
        "k" : "ك",
        "K" : "ك",
        "l" : "ل",
        "L" : "ل",
        "m" : "م",
        "M" : "م",
        "n" : "ن",
        "N" : "ن",
        "h" : "ه",
        "H" : "ه",
        "w" : "و",
        "W" : "و",
        "y" : "ي",
        "Y" : "ي",
        "'" : "ا",
        "g" : "ڨ",
        "G" : "ڨ",
        "p" : "پ",
        "P" : "پ",
        "v" : "ڥ",
        "V" : "ڥ",
        "?" : "؟",
        "!" : "!",
        "," : "،",
        "." : ".",
        "a" : "َ",
        "é" : "َ",
        "è" : "َ",
        "e" : "ِ",
        "i" : "ِ",
        "o" : "ُ",
        "u" : "ُ",
    }

class TunisianSubs(SubsTextTransform):
    """Defines a Transform that substitues latin characters by tunisian ones"""

    # The pattern that matches the command 
    pattern = re.compile(r'tun\|\[(.*?)\]')

    # Matching dictionnary
    matching_dict_priority_0 = {
        "<th>" : "þ",
        "<TH>" : "Þ",

        "<hb>" : "ħ",
        "<HB>" : "Ħ",
        
        "<dh>" : "đ",
        "<DH>" : "Ð",

        "<cdh>" : "đ̧",
        "<CDH>" : "Đ̧",

        "<ct>" : "ţ",
        "<CT>" : "Ţ",

        "<ca>" : "a̧",
        "<CA>" : "A̧",

        "<vs>" : "š",
        "<VS>" : "Š",

        "<cs>" : "ş",
        "<CS>" : "Ş",
        
        "<vr>" : "ř",
        "<VR>" : "Ř",

        "<va>" : "ǎ",
        "<VA>" : "Ǎ",

        "<vo>" : "ǒ",
        "<VO>" : "Ǒ",
        
        "<vi>" : "ǐ",
        "<VI>" : "Ǐ",

        "<A>" : "’",
        "<a>" : "’",
    }

class IPASubs(SubsTextTransform):
    """Defines a Transform that substitues latin characters by IPA ones"""

    # The pattern that matches the command 
    pattern = re.compile(r'ipa\|\[(.*?)\]')

    # Matching dictionnary
    matching_dict_priority_0 = {
        "<th>" : "θ",
        "<TH>" : "θ",
        "<hb>" : "ħ",
        "<HB>" : "ħ",
        "<dh>" : "ð",
        "<DH>" : "ð",
        "<vs>" : "ʃ",
        "<VS>" : "ʃ",
        "<cs>" : "sˤ",
        "<CS>" : "sˤ",
        "<cdh>" : "ðˤ",
        "<CDH>" : "ðˤ",
        "<ct>" : "tˤ",
        "<CT>" : "tˤ",
        "<cdh2>" : "ðˤ",
        "<CDH2>" : "ðˤ",
        "<ca>" : "ʕ",
        "<CA>" : "ʕ",
        "<vr>" : "ɾ",
        "<VR>" : "ɾ",
        "<A>" : "ʔ",
        "<I>" : "ʔ",
        "<->" : "ʔ",
        "<va>" : "ɑ̃",
        "<vo>" : "ɔ̃",
        "<vi>" : "ɛ̃",
    }
    matching_dict_priority_1 = {
        "b" : "b",
        "B" : "b",
        "t" : "t",
        "T" : "t",
        "j" : "ʒ",
        "J" : "ʒ",
        "x" : "χ",
        "X" : "χ",
        "d" : "d",
        "D" : "d",
        "r" : "ɾ",
        "R" : "ɾ",
        "z" : "z",
        "Z" : "z",
        "s" : "s",
        "S" : "s",
        "f" : "f",
        "F" : "f",
        "q" : "q",
        "Q" : "q",
        "k" : "k",
        "K" : "k",
        "l" : "l",
        "L" : "l",
        "m" : "m",
        "M" : "m",
        "n" : "n",
        "N" : "n",
        "h" : "ɦ",
        "H" : "ɦ",
        "w" : "w",
        "W" : "w",
        "y" : "j",
        "Y" : "j",
        "g" : "g",
        "G" : "g",
        "p" : "p",
        "P" : "p",
        "v" : "v",
        "V" : "v",
        "a" : "a",
        "é" : "ɪ",
        "è" : "ɛ",
        "e" : "ə",
        "i" : "i",
        "o" : "ɔ",
        "u" : "u",
        "'" : "ˈ",
        ":" : "ː",
    }


# To qualify the file as an extension
def setup(app):
    app.add_transform(TunisianSubs)
    app.add_transform(ArabSubs)
    app.add_transform(IPASubs)