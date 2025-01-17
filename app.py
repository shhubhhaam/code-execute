import streamlit as st
import subprocess
import os
import uuid

# Set up the folder to save files
UPLOAD_FOLDER = "files"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Streamlit app title
st.title("Python Execution Interface")

# Text area for Python code input
code = st.text_area("Write your Python code here", height=300)

# Button to execute code
if st.button("Run Code"):
    if code.strip() == "":
        st.warning("Please enter some Python code.")
    else:
        # Save the code to a temporary file
        temp_filename = f'temp_{uuid.uuid4().hex}.py'
        temp_filepath = os.path.join(UPLOAD_FOLDER, temp_filename)
        with open(temp_filepath, 'w') as f:
            f.write(code)
        
        try:
            # Execute the Python code
            result = subprocess.run(
                ['python', temp_filepath],
                capture_output=True,
                text=True,
                timeout=10  # Set a timeout to avoid infinite loops
            )
            output = result.stdout or result.stderr
            st.success("Execution Output:")
            st.code(output)
        except Exception as e:
            st.error(f"Error during execution: {str(e)}")
        finally:
            # Clean up the temporary file
            if os.path.exists(temp_filepath):
                os.remove(temp_filepath)

# Button to save the code
filename = st.text_input("Filename to save", value="code.py")
if st.button("Save Code"):
    if code.strip() == "":
        st.warning("Please enter some Python code.")
    else:
        save_path = os.path.join(UPLOAD_FOLDER, filename)
        with open(save_path, 'w') as f:
            f.write(code)
        st.success(f"File saved successfully as {filename}.")
        st.markdown(f"[Download {filename}](files/{filename})", unsafe_allow_html=True)

# File downloader
st.markdown("---")
st.header("Download Saved Files")
files = os.listdir(UPLOAD_FOLDER)
if files:
    for file in files:
        file_path = os.path.join(UPLOAD_FOLDER, file)
        with open(file_path, "rb") as f:
            st.download_button(
                label=f"Download {file}",
                data=f,
                file_name=file,
                mime="text/x-python"
            )
else:
    st.info("No saved files available for download.")
