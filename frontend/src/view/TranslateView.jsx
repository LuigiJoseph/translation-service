import React from 'react';
import { Box, Heading, Flex, useColorModeValue } from '@chakra-ui/react';


import LanguageSelector from '../components/LanguageSelector';
import ModelSelector from '../components/ModelSelector';
import TranslationTextarea from '../components/TranslationTextarea';
import TranslateButton from '../components/TranslateButton';

const TranslationView = ({
  text,
  setText,
  translatedText,
  sourceLanguage,
  setSourceLanguage,
  targetLanguage,
  setTargetLanguage,
  model,
  setModel,
  handleTranslate,
}) => {
  const languages = [
    { code: 'ar', name: 'Arabic' },
    { code: 'tr', name: 'Turkish' },
    { code: 'en', name: 'English' },
  ];

  const models = [
    { id: 'qwen', name: 'Qwen' },
    { id: 'helsinki', name: 'Helsinki' },
  ];

  const swapLanguages = () => {
    setSourceLanguage(targetLanguage);
    setTargetLanguage(sourceLanguage);
    setText(translatedText);
  };

  // Dynamic styling for light & dark mode
  const bgColor = useColorModeValue('white', 'gray.800');
  const textColor = useColorModeValue('gray.900', 'white');
  const pageBg = useColorModeValue('gray.100', 'gray.900');

  return (
    <Flex
      direction="column"
      align="center"
      justify="center"
      h="100vh"
      bg={pageBg}
    >
    <Heading
      size="2xl"
      mb={6}
      color={textColor}
      _hover={{
        textShadow: '0px 0px 10px rgba(111, 103, 103, 0.2)',  // Adds shadow effect on hover
      }}
      fontFamily="'Roboto', sans-serif"  // Custom font family
    >
      Translation Service
    </Heading>

      <Box
        w="100%"
        maxW="1000px"
        p={6}
        borderRadius="lg"
        bg={bgColor}
        boxShadow="lg"
      >
        <Flex justify="space-between" align="center" mb={4}>
          <LanguageSelector
            sourceLanguage={sourceLanguage}
            setSourceLanguage={setSourceLanguage}
            targetLanguage={targetLanguage}
            setTargetLanguage={setTargetLanguage}
            languages={languages}
            swapLanguages={swapLanguages}
          />

          <ModelSelector model={model} setModel={setModel} models={models} />
        </Flex>

        <Flex gap={4}>
          <TranslationTextarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Type or paste text here..."
          />
          <TranslationTextarea
            value={translatedText}
            placeholder="Translation will appear here..."
            isReadOnly
          />
        </Flex>

        <TranslateButton onClick={handleTranslate} />
      </Box>
    </Flex>
  );
};

export default TranslationView;