import { useState } from 'react';

const useTranslationModel = () => {
  const [text, setText] = useState('');
  const [translatedText, setTranslatedText] = useState('');
  const [sourceLanguage, setSourceLanguage] = useState('en'); 
  const [targetLanguage, setTargetLanguage] = useState('ar'); 
  const [model, setModel] = useState('helsinki');

  return {
    text,
    setText,
    translatedText,
    setTranslatedText,
    sourceLanguage, 
    setSourceLanguage,
    targetLanguage, 
    setTargetLanguage,
    model,
    setModel,
  };
};

export default useTranslationModel;
