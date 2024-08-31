# pyiBook
A CLI tool for interacting with your local Apple iBooks library for **MacOS users**.
![PyPI - Version](https://img.shields.io/pypi/v/pyiBook?logo=Pypi)
![GitHub License](https://img.shields.io/github/license/higher-bottle/pyiBook?logo=GitHub)  
> [!NOTE]
> The functionality that output the highlights in Apple iBook on iPhone will be updated in the future.  

The tool is designed to __extract the notes and highlights__ you have made in Apple Book and __download as CSV or XLSX files__.  
The output will contain:
- Highlighted Content
- Highlight Styles (eg. Underline, Yellow)
- Notes (if you add)
- Modification Date

Output Example:  
<img  alt="image" src="https://github.com/user-attachments/assets/fab61dd3-5c57-4362-bfe8-91a5cd0220ae">

- [Installation](#Installation)
- [Instruction](#Instruction)
  - [Show the overview of files in your local Apple iBook library](#Show-the-overview-of-files-in-your-local-Apple-iBook-library)
  - [Output files which contain highlights and notes](#Output-files-which-contain-highlights-and-notes)
  - [Manually input the path](#Manually-input-the-path)


## Installation
> [!IMPORTANT]
> Please ensure that the version of the python on your pc is **>=3.9**, you can check it by inputting ```python3 --version``` or ```python --version```. You can install or upgrade python according to [Use python on Mac](https://docs.python.org/zh-cn/3.12/using/mac.html) or [Homebrew](https://brew.sh)


It is easy to download the package.  
Just input ```pip install pyiBook``` or ```pip install git+https://github.com/higher-bottle/pyiBook.git``` in Terminal.app.  
After the package is downloaded, you can get started!

## Instruction

If you input ```pyibook highlights --help``` in Terminal.app, you can get the help below. 
```
  Print or output iBook highlights based on the specified criteria.  
  
Options:  
  --all            Print all records.  
  --all-book       Print all book records.  
  --all-pdf        Print all pdf records.  
  --bookname TEXT  Print records with the specified book names (comma-separated).  
  -output          Output the result to a CSV file.  
  --help           Show this message and exit.
```

At the beginning, it will ask you ```Do you want to use the default path of Apple Book(Recommend)? (Y/N) [Y]```, you can choose ```y``` for most time because it is programmed to locate the directory automatically.  
> [!IMPORTANT]
> However, if it warns that ```The path is not valid. Please try another one.```, you have to manually input the path, please refer to [Manually input the path](#Manually-input-the-path).


### Show the overview of files in your local Apple iBook library
The overview will show the bookname, numbers of highlights, author, and filetype of each book.
> [!TIP]
> If you open and upload your PDF files to Apple Books, these files will also be loaded in this library.

```pyibook highlights --all```  print an overview of all the pdf and books.  
```pyibook highlights --all-book```  print an overview of all the books.  
```pyibook highlights --all-pdf```  print an overview of all the pdfs.  
```pyibook highlights --bookname = "book 1, book2, book3"```  print an overview of all the specified books.  
> [!WARNING]
> Please input the fullname of the specified book correctly, or the tool will print ```Cannot find the following books: <unfound book name>```

E.g:
<img width="1000" alt="image" src="https://github.com/user-attachments/assets/59d8bb70-6649-479c-954c-1c8865c06198">

### Output files which contain highlights and notes
Add ``` -output``` after the commands above, then it will output files for the specified books. You can decide which filetype to be exported(.csv/.xlsx) and the file name. 
> [!CAUTION]
> If you input a file name which already exists in the folder you are working, it will 
replace it automatically, please pay attention to that.


For example, ```pyibook highlights --all-book -output``` will export the highlights and notes of all the books. **The generated files will be located in the directory where you run the command.**

### Manually input the path
If the tool asks you to change the path, it may because the given path does not exist or there is no valid database under that.  
1. To resolve it, you can input ```BKLibrary``` in the Spotlight Search of on your macbook and check if there is some databases with suffiex ".sqlite" in this folder.
2. If all of those conditions are met, please input the absolute path of its **parent folder**.
