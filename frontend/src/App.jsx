import React from 'react';
import { ChakraProvider, IconButton, useColorMode , Box, useToast} from '@chakra-ui/react';
import { MoonIcon, SunIcon } from '@chakra-ui/icons';

import useTranslationModel from './TranslationModel';
import TranslationService from './TranslationService';
import TranslationView from './view/TranslateView';


const App = () => {
    const {
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
    } = useTranslationModel();
    
    const toast = useToast();

    const { colorMode, toggleColorMode } = useColorMode(); // Use the hook

    const handleTranslate = async () => {
        console.log("Sending translation request with:");
        console.log("Text:", text);
        console.log("Model:", model);
        console.log("Source Language:", sourceLanguage);
        console.log("Target Language:", targetLanguage);
      
        // Check if the source and target languages are the same
        if (sourceLanguage === targetLanguage) {
          toast({
            title: 'Error',
            description: 'Source and target languages cannot be the same.',
            status: 'error',
            duration: 3000,
            isClosable: true,
          });
          return; 
        }
      
        try {
          const translatedText = await TranslationService.translate(
            text,
            model,
            sourceLanguage,
            targetLanguage
          );
          setTranslatedText(translatedText);
        } catch (error) {
          toast({
            title: 'Error',
            description: error.response?.data?.message || error.message || "An error occurred.",
            status: 'error',
            duration: 3000,
            isClosable: true,
          });
        }
      };
      
  
    return (
      <>
        {/* Dark Mode Toggle Button */}
        <Box position="absolute" top={4} right={4}>
          <IconButton
            aria-label="Toggle dark mode"
            icon={colorMode === 'light' ? <MoonIcon /> : <SunIcon />} // Toggle between MoonIcon and SunIcon
            onClick={toggleColorMode} // Call toggleColorMode on click
          />
        </Box>
  
        {/* Translation View */}
        <TranslationView
          text={text}
          setText={setText}
          translatedText={translatedText}
          sourceLanguage={sourceLanguage}
          setSourceLanguage={setSourceLanguage}
          targetLanguage={targetLanguage}
          setTargetLanguage={setTargetLanguage}
          model={model}
          setModel={setModel}
          handleTranslate={handleTranslate}
        />
      </>
    );
  };
  
  export default App;