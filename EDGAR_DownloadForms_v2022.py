"""
    Program to download EDGAR files by form type
    Dependencies (i.e., modules you must already have downloaded)
      EDGAR_Forms_v####.py
      EDGAR_Pac_v####.py
      General_Utilities_v####.py

ND-SRAF / McDonald : 202201
https://sraf.nd.edu
"""

import datetime as dt
import os
import requests
import sys
import time
# These modules must be in the same folder as this code (or use a sys.path.append())
import MOD_EDGAR_Forms  # This module contains some predefined form groups
import MOD_Download_Utilities as du


# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * +

#  NOTES
#        The EDGAR archive contains millions of forms.
#        For details on accessing the EDGAR servers see:
#          https://www.sec.gov/edgar/searchedgar/accessing-edgar-data.htm
#        From that site:
#            "To preserve equitable server access, we ask that bulk FTP
#             transfer requests be performed between 9 PM and 6 AM Eastern 
#             time. Please use efficient scripting, downloading only what you
#             need and space out requests to minimize server load."
#        Note that the program will check the clock every 10 minutes and only
#            download files during the appropriate time.
#        Be a good citizen...keep your requests targeted.
#
#        For large downloads you will sometimes get a hiccup in the server
#            and the file request will fail.  These errs are documented in
#            the log file.  You can manually download those files that fail.
#            Although I attempt to work around server errors, if the SEC's server
#            is sufficiently busy, you might have to try another day.
#
#       For a list of form types and counts by year:
#         "All SEC/EDGAR Filings Tabulation" in https://sraf.nd.edu


# -----------------------
# User defined parameters
# -----------------------
# List target forms as strings separated by commas (case sensitive) or
#   load from EDGAR_Forms.  (See EDGAR_Forms module for predefined lists.)
PARM_FORMS = {'10-K'} #MOD_EDGAR_Forms.f_10X  # or, for example, PARM_FORMS = ['8-K', '8-K/A']
PARM_COMPANY = ['United Airlines Holdings, Inc.']
PARM_BGNYEAR = 1993  # User selected bgn period.  Earliest available is 1993 
PARM_ENDYEAR = 2024  # User selected end period.
PARM_BGNQTR = 1  # Beginning quarter of each year
PARM_ENDQTR = 4  # Ending quarter of each year
# Path where you will store the downloaded files
PARM_PATH = r'C:\Users\Nate\Documents\Code\School\TestFolder'
# Change the file pointer below to reflect your location for the log file
#    (directory must already exist)
PARM_LOGFILE = (r'C:\Users\Nate\Documents\Code\School\TestFolder\EDGAR_Download_FORM-X_LogFile_' +
                str(PARM_BGNYEAR) + '-' + str(PARM_ENDYEAR) + '.txt')
# EDGAR parameter
PARM_FORM_PREFIX = 'https://www.sec.gov/Archives/'
PARM_MASTERIDX_PREFIX = 'https://www.sec.gov/Archives/edgar/full-index/'
# Server parms
HEADER = {'Host': 'www.sec.gov', 'Connection': 'close',
         'Accept': 'application/json, text/javascript, */*; q=0.01', 'X-Requested-With': 'XMLHttpRequest',
         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
         }
#
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * +
print(MOD_EDGAR_Forms.f_10X)

def download_forms():
    f_log = open(PARM_LOGFILE, 'a')
    f_log.write('BEGIN LOOPS:  {0}\n'.format(time.strftime('%c')))
    n_tot = 0
    n_errs = 0
    
    for year in range(PARM_BGNYEAR, PARM_ENDYEAR + 1):
        for qtr in range(PARM_BGNQTR, PARM_ENDQTR + 1):
            print(year, qtr)
            startloop = dt.datetime.now()
            n_qtr = 0
            file_count = dict()
            path = '{0}{1}\\QTR{2}\\'.format(PARM_PATH, str(year), str(qtr))
            print(path)
            
            if not os.path.exists(path):
                os.makedirs(path)
                print(f'Path: {path} created')
            
            sec_url = f'{PARM_MASTERIDX_PREFIX}{year}/QTR{qtr}/master.idx'
            masterindex = du.download_to_doc(sec_url)
            
            if masterindex:
                # Print the first few lines to check if the content is as expected
                print("Raw master index content:")
                print(masterindex[:2000])  # Print first 2000 characters for inspection
                
                lines = masterindex.splitlines()
                
                # Print the total number of lines for inspection
                print(f"Total lines in master index: {len(lines)}")
                
                # Skip header lines and additional lines before data
                header_lines_count = 11
                if len(lines) > header_lines_count:
                    lines = lines[header_lines_count:]
                else:
                    print("Not enough lines to skip header.")
                    continue
                
                # Print lines after header
                # print("Lines after header:")
                # print("\n".join(lines[:20]))  # Print first 20 lines after header for inspection
                
                # Find the start of the data section
                # while lines and not lines[0].strip().startswith('CIK|'):
                #     lines.pop(0)  # Remove lines until we find the start of the data
                
                # Skip the separator line after header
                if lines and lines[0].strip() == '--------------------------------------------------------------------------------':
                    lines.pop(0)
                
                # Print lines before processing
                # print("Lines to process:")
                # print("\n".join(lines[:20]))  # Print first 20 lines to process for inspection
                
                # print(f"Data lines count: {len(lines)}")
                
                # Process each line
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue  # Skip empty lines
                    # print(line)
                    # print(f"Processing line: '{line}'")
                    item = MasterIndexRecord(line)
                    
                    if item.err:
                        print(f"Error with line: {line}")
                        f_log.write(f"Error with line: {line}\n")
                        continue

                    # if item.name:
                    #     print(f'Item Name: {item.name}')
                    #     continue

                    if  item.form in PARM_FORMS and item.name in PARM_COMPANY:
                        print(item.name)
                        n_qtr += 1
                        fid = str(item.cik) + str(item.filingdate) + item.form
                        if fid in file_count:
                            file_count[fid] += 1
                        else:
                            file_count[fid] = 1
                        url = PARM_FORM_PREFIX + item.path
                        # print(url)
                        fname = (path + str(item.filingdate) + '_' + item.form.replace('/', '-') + '_' +
                                 item.path.replace('/', '_'))
                        fname = fname.replace('.txt', '_' + str(file_count[fid]) + '.txt')
                        try:
                            return_url = du.download_to_file(url, fname, f_log=f_log)
                            if return_url:
                                n_errs += 1
                        except Exception as e:
                            print(f"Error downloading file from {url}: {e}")
                            f_log.write(f"Error downloading file from {url}: {e}\n")
                            n_errs += 1
                        
                        n_tot += 1
                        if n_tot % 100 == 0:
                            print(f'  Total files: {n_tot:,}', end="\r")
                        time.sleep(1)  # Space out requests
            
            print(f'{year} : {qtr} -> {n_qtr:,} downloads completed.  Time = ' + \
                  f'{(dt.datetime.now() - startloop)}' + \
                  f' | {dt.datetime.now()}')
            f_log.write(f'{year} | {qtr} | n_qtr = {n_qtr:>8,} | n_tot = {n_tot:>8,} | n_err = {n_errs:>6,} | ' +
                        f'{dt.datetime.now()}\n')
            f_log.flush()

    print('{0:,} total forms downloaded.'.format(n_tot))
    f_log.write('\n{0:,} total forms downloaded.'.format(n_tot))
    f_log.close()

class MasterIndexRecord:
    def __init__(self, line):
        self.err = False
        parts = line.strip().split('|')
        if len(parts) == 5:
            try:
                self.cik = int(parts[0])
                self.name = parts[1]
                self.form = parts[2]
                self.filingdate = int(parts[3].replace('-', ''))
                self.path = parts[4]
            except ValueError as e:
                self.err = True
                print(f"ValueError parsing line: {line} | Error: {e}")
        else:
            self.err = True
            print(f"Incorrect number of parts in line: {line}")




if __name__ == '__main__':
    start = dt.datetime.now()
    print(f"\n\n{start.strftime('%c')}\nPROGRAM NAME: {sys.argv[0]}\n")
    
    download_forms()
    
    print(f'\n\nRuntime: {(dt.datetime.now()-start)}')
    print(f'\nNormal termination.\n{dt.datetime.now().strftime("%c")}\n')
