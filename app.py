import streamlit as st
from streamlit_image_select import image_select
from table import main
import numpy as np
from PIL import Image
from streamlit_paste_button import paste_image_button as pbutton

# Use PIL for reading image from the user as an object instead of cv2 -> reads img using path as an array

def info():
    with st.expander("**Eager to know how it works??**", ):
        st.info("""
                    **1. Tabular Region Detection:** It first detects tabular regions within given input images by performing a sequence of OpenCV operations. 
                    
                    **2. Text Extraction:** Building upon the detection of tabular regions, this app evaluate ***EasyOCR's*** efficacy in accurately extracting text data located within these identified tabular regions.
                    
                    **3. Tabular Conversion:** In addition to text extraction, this application converts the extracted text data back into a tabular format accurately. 
                """)

def user_selection(image_file, paste_btn):
        try:
            if image_file is not None:
                st.image(image_file, caption="Input Image")
                if st.button("Start", key = 1):
                    image = np.array(Image.open(image_file))
            elif paste_btn.image_data is not None:
                st.image(paste_btn.image_data,"Input")
                if st.button("Start", key = 2):
                    image = np.array(paste_btn.image_data)
            with st.spinner(text='In progress'):
                output = main(image)  # Header, Result, BBox, RoI, df
                st.image(output[2], caption="Bounding Box Information")
                st.image(output[3], caption="Region of Interest")
                st.markdown("## Tabular Form")
                if output[0] is not None:
                    st.write(output[0])
                st.dataframe(output[4])
            st.write("Process Completed")
            info()
                
        except UnboundLocalError:
            st.error("Stay cool! Start Processing.")
        except AttributeError:
            st.error("Stay cool! Start Processing.")
        except FileNotFoundError:
            st.write("Please Upload an Image to detect Objects")
        except RuntimeError:
            st.error("Unexpected Input Image Format. No Detections 🙄")
        except:
            st.write("Stay Cool and Begin Processing 😜")
  
def default():
    try:
        images = ["input1.png", "input2.png"]
        st.markdown("### Start with default images")

        clicked = image_select("Select an Image", images, key = "k1")
        st.image(clicked, caption="Input Image")
        if st.button("Start", key = "1"):
            clicked = np.array(Image.open(clicked))
            with st.spinner(text='In progress'):
                output = main(clicked)  # Header, Result, BBox, RoI, df
                st.image(output[2], caption="Bounding Box Information")
                st.image(output[3], caption="Region of Interest")
                st.markdown("## Tabular Form")
                if output[0] is not None:
                    st.write(output[0])
                st.dataframe(output[4])
            st.write("Process Completed")
            info()

    except UnboundLocalError:
        st.error("Stay cool! Start Processing.1")
    except AttributeError:
        st.error("Stay cool! Start Processing.2")
    except TypeError:
        st.error("Table Data Not Present in the given image")
    except Exception:
        st.error(st.error("Stay cool! Start Processing.3"))
    except:
        st.write("sjg")

def start():

    st.markdown("## Extracting Table Content from an Image")
    st.info('Avoid loading images that are Blured, Containing Watermarks/background information or tables with too many Missing Values, as it may results with No Detections/Misplacement of data items.', icon="ℹ️")

    sidebar_action = 0

    with st.sidebar:
        st.subheader("Upload Your Image")
        image_file = st.sidebar.file_uploader("", type=["png","jpg","jpeg"])
    
        # st.subheader("Or")
        st.subheader("Paste an Image")
        paste_btn = pbutton(
        label="📋 Paste an image",
        text_color="#ffffff",
        background_color="#FF0000",
        hover_background_color="#380909",
    )

        if (image_file is None) and (paste_btn.image_data is None):
            sidebar_action = 1        
    
        if paste_btn.image_data is not None:
            st.warning("Suggested to Clear Selection Before Loading New Image", icon='🚨')
            st.write(f'Want to Clear Selection? <a href="{st.session_state.get("url", "")}" target="_self">Click Here</a>', unsafe_allow_html=True)
        
    if (sidebar_action == 0):
        out = user_selection(image_file, paste_btn)
    elif (sidebar_action == 1):
        out = default()
        # pass


start()