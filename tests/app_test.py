import checklist


class TestApp:

    '''Checklist'''

    def test_substitute_qa(self):
        '''adds a TAB after Q. and A.'''

        raw = "\nQ. And for purposes of today, may I call you Amber? Or do you prefer Ms. Hard?\nA. Amber is fine.\nQ. And Amber, have you given a deposition before?\nA. Yes."
        final = "\nQ.\tAnd for purposes of today, may I call you Amber? Or do you prefer Ms. Hard?\nA.\tAmber is fine.\nQ.\tAnd Amber, have you given a deposition before?\nA.\tYes."
        assert checklist.substitute_qa(raw) == final


    def test_substitute_colloquy(self):
        '''adds double spaces after speaker IDs in colloquy'''

        raw = "\nMR. REDDINGTON: Mr. Court Reporter, can we take a five-minute break, please?\nTHE REPORTER: Okay. The time is 10:32 a.m., and we are off the record.\n"
        final = "\nMR. REDDINGTON:  Mr. Court Reporter, can we take a five-minute break, please?\nTHE REPORTER:  Okay. The time is 10:32 a.m., and we are off the record.\n"

        assert checklist.substitute_colloquy(raw) == final


    def test_substitute_by_line_colon(self):
        '''adds colons to by-lines'''

        raw = "\nBY MR. REDDINGTON\nBY MS. KEEN\n"
        final = "\nBY MR. REDDINGTON:\nBY MS. KEEN:\n"

        assert checklist.substitute_by_line_colon(raw) == final


    def test_substitute_punctuation_one_space(self):
        '''substitutes single spaces after sentence-ending punctuation to double spaces'''

        text = "Hello, Mark. How are you doing today? Are you psyched up for today?"
        assert checklist.substitute_punctuation_one_space(text) == "Hello, Mark.  How are you doing today?  Are you psyched up for today?"


    def test_substitute_strike_that(self):
        '''moves text after 'strike that' to a new line'''

        raw = "Q. As a mother --strike that.  How old are you?\nA. 34.\n"
        final = "Q. As a mother --strike that.  \n\t\tHow old are you?\nA. 34.\n"

        assert checklist.substitute_strike_that(raw) == final


    def test_substitute_double_colon(self):
        '''removes double colons in by-lines, etc.'''
        
        raw = "\nBY MR. REDDINGTON::\nBY MS. KEEN:\n"
        final = "\nBY MR. REDDINGTON:\nBY MS. KEEN:\n"

        assert checklist.substitute_double_colon(raw) == final


    def test_format_tabs(self):
        '''adds two TABs before colloquy IDs and one TAB before QA'''

        raw = "\nQ. Did you see Mr. Doe?\nA. No.\nMR. REDDINGTON:  I have no further questions.\nMS. KEEN:  Can we take a break?\n"
        final = "\tQ. Did you see Mr. Doe?\n\tA. No.\n\t\tMR. REDDINGTON:  I have no further questions.\n\t\tMS. KEEN:  Can we take a break?\n"

        print(final)
        assert checklist.format_tabs(raw) == final

    def test_format_parentheticals(self):
        '''adds two TABS to parentheticals'''

        raw = "\nTHE REPORTER: The time is 11:02 a.m., and we are off the record.\n(Off the record.)\nTHE REPORTER: We are back on the record. The time is 11:05 a.m.\n"
        final = "\nTHE REPORTER: The time is 11:02 a.m., and we are off the record.\n\t\t(Off the record.)\nTHE REPORTER: We are back on the record. The time is 11:05 a.m.\n"

        assert checklist.format_parentheticals(raw) == final
