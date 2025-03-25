import axios from 'axios';

const translateText = async (text, model, sourceLanguage, targetLanguage) => {
  try {
    const payload = {
      text,  
      model,  
      source_locale: sourceLanguage, 
      target_locale: targetLanguage, 
    };

    console.log(" Sending Payload:", payload); 

    const response = await axios.post(
      'http://localhost:5000/translation-endpoints/api/v1/translate',
      payload,
      { headers: { 'Content-Type': 'application/json' } }  
    );

    console.log(" Response from Server:", response.data);

    return response.data.translated_text;
    
  } catch (error) {
    console.error("Translation Error:", error.response?.data || error.message);
    throw new Error(`Translation failed: ${error.response?.data?.message || error.message}`);
  }
};

export default translateText;
