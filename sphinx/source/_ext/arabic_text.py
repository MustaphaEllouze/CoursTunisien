import re
from sphinx.transforms import SphinxTransform
from docutils import nodes

class SubsTextTransform(SphinxTransform):
    """Base classe that Defines a Transform that substitues latin characters 
    by unicode characters"""

    default_priority = 500  # Runs at a typical priority level

    # The pattern that matches the command 
    pattern = re.compile(r'command\|`([^`]+)`')

    # Matching dictionnary
    matching_dict_priority_0 = {}
    matching_dict_priority_1 = {}

    def apply(self):
        # Iterate over all text nodes in the document
        for node in self.document.traverse(nodes.Text):
            
            # Replaces the text if applicable
            new_text = self.replace_command(
                command_pattern=self.pattern, 
                text=node.astext(),
            )
            
            # Replace in the build
            if new_text != node.astext():
                node.parent.replace(node, nodes.Text(new_text))

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
    pattern = re.compile(r'arab\|`([^`]+)`')

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
        "<t>" : "ط",
        "<T>" : "ط",
        "<cdh2>" : "ظ",
        "<CDH2>" : "ظ",
        "<ca>" : "ع",
        "<CA>" : "ع",
        "<vr>" : "غ",
        "<VR>" : "غ",
        "<A>" : "أ",
        "<I>" : "إ",
        "<W>" : "ؤ",
        "<O>" : "ئ",
        "<Y>" : "ى",
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
        "@" : "ة",
        "'" : "ا",
        "g" : "ڨ",
        "G" : "ڨ",
        "p" : "پ",
        "P" : "پ",
        "v" : "ڥ",
        "V" : "ڥ",
        "~" : "ّ",
        "?" : "؟",
        "!" : "!",
        "," : "،",
        "." : ".",
    }

class TunisianSubs(SubsTextTransform):
    """Defines a Transform that substitues latin characters by tunisian ones"""

    # The pattern that matches the command 
    pattern = re.compile(r'tun\|`([^`]+)`')

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
    }

# To qualify the file as an extension
def setup(app):
    app.add_transform(TunisianSubs)
    app.add_transform(ArabSubs)