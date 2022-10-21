import re
import tkinter
import tkinter.ttk as ttk
from tkinter.filedialog import askopenfilenames, asksaveasfilename

import checklist

from formation import AppBuilder


class FormatApp(AppBuilder):
    filetypes = (
        ('text files', '*.txt'),
        ('All files', '*.*')
    )

    def __init__(self):
        self.scroll_y: ttk.Scrollbar = None
        self.main_text: tkinter.Text = None

        super().__init__(path="main_ui.xml")
        self.connect_callbacks(self)
        self.main_text.config(yscrollcommand=self.scroll_y.set)
        self.scroll_y.config(command=self.main_text.yview)

        self.mutators = (
        checklist.substitute_qa,
        checklist.substitute_colloquy,
        checklist.substitute_by_line_colon,
        checklist.substitute_punctuation_one_space,
        checklist.substitute_title_abbreviations,
        checklist.substitute_strike_that,
        checklist.substitute_double_colon,
        checklist.format_tabs,
        checklist.format_parentheticals,
        checklist.substitute_new_speaker,
        checklist.substitute_words,
        )

        self._highlighters = (
            self._fmt_by_line,
            self._fmt_colloquy,
            self._fmt_qa,
            self._fmt_strike_that,
            self._fmt_parenthetical,
            self._fmt_abbrev,
            self._fmt_invalid_qa,
            self._fmt_joint,
            self._fmt_examination_heading
        )

        self._app.title('PyCheck Auto-Formatter')

        try:
            self._app.state('zoomed')
        except:
            self._app.wm_attributes('-zoomed', True)

        self.main_text.tag_config('by-line', foreground='#7271f0', font='SystemDefault 10 bold')
        self.main_text.tag_config('colloquy', foreground='#A3E635', font='SystemDefault 10 bold')
        self.main_text.tag_config('qa', foreground='orange', font='SystemDefault 10 bold')
        self.main_text.tag_config('file-joint', background="#353570")
        self.main_text.tag_config('strike-that', background="#66C05A")
        self.main_text.tag_config('parenthetical', foreground='magenta', font='SystemDefault 10')
        self.main_text.tag_config('abbrev', background='#e8a9a9')
        self.main_text.tag_config('invalid-qa', background='#ED594A')
        self.main_text.tag_config('examination-heading', foreground='red', font='SystemDefault 10 bold')


    def copy(self):
        self.main_text.clipboard_clear()
        self.main_text.clipboard_append(self.main_text.get("1.0", "end"))

    def save(self):
        file = asksaveasfilename(
            title='Save as',
            confirmoverwrite=True,
            initialdir='.',
            filetypes=FormatApp.filetypes
        )

        if file:
            with open(file, 'w') as out:
                out.write(self.main_text.get('0.0', 'end'))

    def refresh(self):
        for tag in self.main_text.tag_names():
            self.main_text.tag_remove(tag, '0.0', 'end')
        self.text = self.main_text.get('0.0', 'end')
        self.highlight()
        self.remove_start_markers()

    def open(self):
        self.filenames = askopenfilenames(
            title='Open file',
            initialdir='.',
            defaultextension='.txt',
            filetypes=FormatApp.filetypes
        )
        if self.filenames:
            self.reformat()

    def reformat(self):
        self.text = ""
        for file in self.filenames:
            with open(file, 'r') as f:
                self.text += "\n{{{" + f.read()
        self.text = self.text.lstrip("\n")

        for mutator in self.mutators:
            self.text = mutator(self.text)

        for tag in self.main_text.tag_names():
            self.main_text.tag_remove(tag, '0.0', 'end')
        self.main_text.delete('0.0', 'end')

        self.main_text.insert('0.0', self.text)
        self.highlight()
        self.remove_start_markers()

    def remove_start_markers(self):
        correction = 0
        for m in re.finditer(r'\{\{\{', self.text):
            self.main_text.delete(
                f'0.0 + {m.span()[0] - correction} chars', f'0.0 + {m.span()[1] - correction} chars'
            )
            correction += 3

    def highlight(self):
        for h in self._highlighters:
            h()

    def _fmt_by_line(self):
        for m in re.finditer(r'\n(BY.+:)\n', self.text):
            self.main_text.tag_add('by-line', f'0.0 + {m.span()[0]} chars', f'0.0 + {m.span()[1]} chars')

    def _fmt_colloquy(self):
        for m in re.finditer(r'\t\t(.+:)  ', self.text):
            self.main_text.tag_add('colloquy', f'0.0 + {m.span()[0]} chars', f'0.0 + {m.span()[1]} chars')

    def _fmt_qa(self):
        for m in re.finditer(r'\t([QA].)\t', self.text):
            self.main_text.tag_add('qa', f'0.0 + {m.span()[0]} chars', f'0.0 + {m.span()[1]} chars')

    def _fmt_strike_that(self):
        for m in re.finditer(r'(--.+(?:rephrase|[sS]trike that))', self.text):
            self.main_text.tag_add('strike-that', f'0.0 + {m.span()[0]} chars', f'0.0 + {m.span()[1]} chars')

    def _fmt_parenthetical(self):
        for m in re.finditer(r'\t\t(\(.+\))', self.text):
            self.main_text.tag_add('parenthetical', f'0.0 + {m.span()[0]} chars', f'0.0 + {m.span()[1]} chars')

    def _fmt_abbrev(self):
        for m in re.finditer(r' ([A-Z]\.) ', self.text):
            self.main_text.tag_add('abbrev', f'0.0 + {m.span()[0]} chars', f'0.0 + {m.span()[1]} chars')

    def _fmt_qa_by_line(self):
        for m in re.finditer(r'(?<=[^:])\n\t(Q\.\t.+)', self.text):
            self.main_text.tag_add('invalid-qa', f'0.0 + {m.span()[0]} chars', f'0.0 + {m.span()[1]} chars')

    def _fmt_invalid_qa(self):
        for m in re.finditer(r'\t(Q\.\t.+\n\tQ\.\t.+)', self.text):
            self.main_text.tag_add('invalid-qa', f'0.0 + {m.span()[0]} chars', f'0.0 + {m.span()[1]} chars')
        for m in re.finditer(r'\t(A\.\t.+\n\tA\.\t.+)', self.text):
            self.main_text.tag_add('invalid-qa', f'0.0 + {m.span()[0]} chars', f'0.0 + {m.span()[1]} chars')

    def _fmt_joint(self):
        for m in re.finditer(r'.+{{{.+', self.text):
            self.main_text.tag_add('file-joint', f'0.0 + {m.span()[0]} chars', f'0.0 + {m.span()[1]} chars')

    def _fmt_examination_heading(self):
        for m in re.finditer(r"\n(.+EXAMINATION)\n", self.text):
            self.main_text.tag_add('examination-heading', f'0.0 + {m.span()[0]} chars', f'0.0 + {m.span()[1]} chars')


if __name__ == '__main__':
    FormatApp().mainloop()
