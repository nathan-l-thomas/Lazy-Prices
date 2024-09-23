# Lazy Prices

## Weekly Updates

## 9/22/2024
- Added additional scripts from the University of Norte Dame
- Added an HTML parsing script to do the following:
- Remove unnecessary ASCII-encoded segments
- Strip out specific HTML tags like `<DIV>`, `<TR>`, `<TD>`, and `<FONT>`
- Delete all XML and XBRL content
- Replace non-breaking spaces and ampersand references.
- Remove tables based on character content
- Tag exhibits for later processing
- Clean up remaining markup tags and excess line feeds

### 9/8/2024
- Added Program to download EDGAR files from the SEC site by form type from University of Norte Dame
- Modfied script to add increased error handling
- Modifed script to increase wait time between requests to decrease download errors
