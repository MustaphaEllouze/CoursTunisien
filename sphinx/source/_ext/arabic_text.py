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
    matching_dict = {}

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
            for initial_char, new_char in self.match_dict.items():
                text_to_subs = text_to_subs.replace(initial_char, new_char)
            return text_to_subs
        return text

class ArabSubs(SubsTextTransform):
    """Defines a Transform that substitues latin characters by arab ones"""

    # The pattern that matches the command 
    pattern = re.compile(r'arab\|`([^`]+)`')

    # Matching dictionnary
    match_dict = {
        "b" : "ب",
        "t" : "ت",
        "C" : "ث",
        "j" : "ج",
        "H" : "ح",
        "x" : "خ",
        "d" : "د",
        "4" : "ذ",
        "r" : "ر",
        "z" : "ز",
        "s" : "س",
        "c" : "ش",
        "S" : "ص",
        "D" : "ض",
        "T" : "ط",
        "Z" : "ظ",
        "G" : "ع",
        "R" : "غ",
        "f" : "ف",
        "q" : "ق",
        "k" : "ك",
        "l" : "ل",
        "m" : "م",
        "n" : "ن",
        "h" : "ه",
        "w" : "و",
        "y" : "ي",
        "@" : "ة",
        "'" : "ا",
        "A" : "أ",
        "I" : "إ",
        "W" : "ؤ",
        "O" : "ئ",
        "Y" : "ى",
        "g" : "ڨ",
        "p" : "پ",
        "v" : "ڥ",
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
    match_dict = {
        r"<th>" : "þ",
        "a" : "aa",
    }

# To qualify the file as an extension
def setup(app):
    app.add_transform(TunisianSubs)
    app.add_transform(ArabSubs)