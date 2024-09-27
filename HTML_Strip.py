# import html.parser
import os
import re


#  * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * #
# - Remove ASCII-Encoded segments – All document segment <TYPE> tags of GRAPHIC, ZIP, EXCEL, JSON, and PDF are deleted from the file. ASCII-encoding is a means of converting binary-type files into standard ASCII characters to facilitate transfer across various hardware platforms. A relatively small graphic can create a substantial ASCII segment. Filings containing multiple graphics can be orders of magnitude larger than those containing only textual information.
# - Remove <DIV>, <TR>, <TD>, and <FONT> tags – Although we require some HTML information for subsequent parsing, the files are so large (and processed as a single string) that, for processing efficiency, we initially simply strip out some of the formatting HTML.
# - Remove all XML – all XML-embedded documents are removed.
# - Remove all XBRL – all characters between <XBRL …> … </XBRL> are deleted.
# - Remove SEC Header/Footer – All characters from the beginning of the original file thru </SEC-HEADER> (or </IMS-HEADER> in some older documents) are deleted from the file. Note however that the header information is retained and included in the tagged items discussed in section 4.1. In addition, the footer “-----END PRIVACY-ENHANCED MESSAGE-----” appearing at the end of each document is deleted.
# - Replace \&NBSP and \&#160 with a blank space.
# - Replace \&AMP and \&#38 with “&”
# - Remove all remaining extended character references (ISO-8859-1, see http://www.sec.gov/info/edgar/edgarfm-vol2-v34.pdf section 5.2.2.6.
# - Remove tables – all characters appearing between <TABLE> and </TABLE> tags are removed.
# - Note that some filers use table tags to demark paragraphs of text, so each potential table string is first stripped of all HTML and then the number of numeric versus alphabetic characters is compared. For this parsing, only table-encapsulated strings where numeric chars/(alphabetic+numeric chars) > 10% are removed.
# - In some instances, Item 7 and/or Item 8 of the filings begins with a table of data where the Item 7 or 8 demarcation appears as a line within the table string. Thus, any table string containing “Item 7” or “Item 8” (case insensitive) is not deleted.
# - Tag Exhibits – At this point in the parsing process all exhibits are tagged as discussed in section 3.2.
# - Remove Markup Tags – remove all remaining markup tags (i.e., <…>).
# - Excess line feeds are removed.
#  * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * #


FOLDER_TO_PARSE = r'C:\Users\Nate\Documents\Code\School\Lazy Prices\RawDocuments'
CLEANED_OUTPUT_FOLDER = r'C:\Users\Nate\Documents\Code\School\Lazy Prices\CleanedDocuments'


class FilingCleaner:
    def __init__(self, content):
        """Initialize with the file content."""
        self.content = content

    def remove_ascii_encoded_segments(self):
        """Remove segments like <TYPE>GRAPHIC and content until 'end'."""
        pattern = r'<TYPE>(GRAPHIC|ZIP|EXCEL|JSON|PDF).*?end'
        self.content = re.sub(pattern, '', self.content,
                              flags=re.DOTALL | re.IGNORECASE)

    def remove_div_tr_td_font_tags(self):
        """Remove <DIV>, <TR>, <TD>, and <FONT> tags."""
        pattern = r'<(DIV|TR|TD|FONT)>'
        self.content = re.sub(pattern, '', self.content,
                              flags=re.IGNORECASE | re.DOTALL)

    def remove_xml_documents(self):
        """Remove all XML-embedded documents."""
        pattern = r'<[^>]+>.*?</[^>]+>'
        self.content = re.sub(pattern, '', self.content, flags=re.DOTALL)

    def remove_sec_header_footer(self):
        """Remove SEC Header/Footer from the document."""
        self.content = re.sub(
            r'^.*?</SEC-HEADER>|^.*?</IMS-HEADER>', '', self.content, flags=re.DOTALL)
        self.content = re.sub(
            r'-----END PRIVACY-ENHANCED MESSAGE-----$', '', self.content, flags=re.DOTALL)

    def replace_nbsp_and_amp_entities(self):
        """Replace &NBSP and &#160 with a blank space, and &AMP and &#38 with “&”."""
        self.content = re.sub(r'\&(NBSP|#160)', '', self.content)
        self.content = re.sub(r'\&(AMP|#38)', '&', self.content)

    def remove_specific_html_entities(self):
        """Remove specific HTML character references."""
        pattern = r'&#(135|136|137|138|139);'
        self.content = re.sub(pattern, '', self.content)

    def remove_tables_based_on_character_ratio(self):
        """Remove tables based on character ratio logic, except those containing 'Item 7' or 'Item 8'."""
        tables = re.findall(r'<TABLE.*?>(.*?)</TABLE>',
                            self.content, flags=re.DOTALL | re.IGNORECASE)

        for table in tables:
            # Check if the table contains "Item 7" or "Item 8"
            if re.search(r'Item 7|Item 8', table, flags=re.IGNORECASE):
                continue  # Skip this table

            numeric_count = sum(c.isdigit() for c in table)
            alphabetic_count = sum(c.isalpha() for c in table)
            total_count = numeric_count + alphabetic_count

            if total_count > 0 and (numeric_count / total_count) > 0.10:
                self.content = self.content.replace(table, '')

        self.content = re.sub(r'<TABLE.*?>\s*</TABLE>', '',
                              self.content, flags=re.DOTALL | re.IGNORECASE)

    def remove_xbrl_content(self):
        """Remove all XBRL – all characters between <XBRL ...> ... </XBRL> are deleted."""
        self.content = re.sub(r'<XBRL.*?>.*?</XBRL>', '',
                              self.content, flags=re.DOTALL | re.IGNORECASE)

    def remove_html_comments(self):
        """Remove HTML comments."""
        self.content = re.sub(r'<!--.*?-->', '', self.content, flags=re.DOTALL)

    def remove_remaining_html_tags(self):
        """Remove any remaining HTML tags."""
        self.content = re.sub(r'<[^>]+>', '', self.content)

    def remove_empty_lines(self):
        self.content = re.sub(r'^\s*\n', '', self.content, flags=re.MULTILINE)

    def clean(self):
        self.remove_ascii_encoded_segments()
        self.remove_div_tr_td_font_tags()
        self.remove_sec_header_footer
        self.replace_nbsp_and_amp_entities()
        self.remove_specific_html_entities()
        self.remove_tables_based_on_character_ratio()
        self.remove_xbrl_content()
        self.remove_html_comments()
        self.remove_remaining_html_tags()
        self.remove_empty_lines()
        return self.content


for root, dirs, files in os.walk(FOLDER_TO_PARSE):
    for file in files:
        if file.endswith('.txt'):
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                print(f'Currently parsing and cleaning <{file}>...')
                file_content = f.read()
                filename_trimmed = file.replace('.txt', '')

                # Clean the content using FilingCleaner
                cleaner = FilingCleaner(file_content)
                cleaned_content = cleaner.clean()  # Clean the file content

                if cleaned_content is None:
                    cleaned_content = ""  # Default to empty string if nothing is returned

                # Define the output file path
                output_filename = f'{filename_trimmed}_cleaned.txt'
                output_path = os.path.join(
                    CLEANED_OUTPUT_FOLDER, output_filename)

                # Write cleaned form to OUTPUT_PATH
                with open(output_path, 'w', encoding='utf-8') as output_file:
                    output_file.write(cleaned_content)
