# PCFileFlicker

# FileFlicker - File Management and QR Code Generation Tool

FileFlicker is a versatile file management application designed to efficiently process, analyze, and manage various types of documents. It enhances user productivity by enabling easy uploads, AI-driven document analysis, and QR code generation for quick access.

## Features

1. **File Uploading**: Users can upload files in various formats including PDF, Word, TXT, and PPTX.
2. **AI Analysis**: Integrates with OpenAI to summarize documents, extract information, and provide intelligent insights.
3. **QR Code Generation**: Generates QR codes for easy access to local server URLs.
4. **Database Management**: Maintains a local database of uploaded files with functionalities to search and manage entries.
5. **Document Scraping**: Allows users to extract and analyze text from URLs.
6. **User-Friendly Interface**: Built with Tkinter for an intuitive and responsive interface.

## Installation

To run the FileFlicker application, ensure you have Python installed along with the following libraries. You can install the dependencies using pip:

```bash
pip install qrcode requests beautifulsoup4 tinydb PyPDF2 python-docx openpyxl python-pptx
```

## Getting Started

1. Clone the repository:
   ```bash
   git clone <your-repository-url>
   cd FileFlicker
   ```

2. Run the application:
   ```bash
   python main.py
   ```

3. Follow the on-screen instructions to upload files and utilize the features.

## Configuration

To configure the application:
- Set your OpenAI API key in the application settings.
- The configuration is stored in `setting/config.json`. Ensure this file exists after the first run.

## Usage

- **Upload Files**: Click on "📤 Upload File" to select files.
- **Search Files**: Use the search bar to filter through your uploaded documents.
- **View File Details**: Double-click on a file entry to view or edit its details.
- **Analyze Files**: Use the AI analysis feature to summarize and extract key data from your documents.


## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Support

For issues or feature requests, please open an issue on the GitHub repository or fill out the [Report Issue](https://docs.google.com/forms/d/13aoyEZhTE3N9M82gWQxRo9Ir8_s3s7YXeQq8rF3-E88) form.

## Acknowledgments

- [OpenAI](https://www.openai.com) for the powerful API.
- The libraries used in this project for contributing essential functionalities.

## Conclusion

FileFlicker is a powerful tool for anyone looking to streamline their document management process. It allows for easy file uploads, intelligent analysis, and convenient QR code generation, all within an intuitive interface.

Feel free to explore the application and enhance your productivity today!
