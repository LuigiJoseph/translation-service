import React from 'react';
import { Select, IconButton, Flex } from '@chakra-ui/react';
import { RepeatIcon } from '@chakra-ui/icons';

const LanguageSelector = ({
  sourceLanguage,
  setSourceLanguage,
  targetLanguage,
  setTargetLanguage,
  languages,
  swapLanguages,
}) => {
  return (
    <Flex gap={4}>
      <Select
        value={sourceLanguage}
        onChange={(e) => setSourceLanguage(e.target.value)}
      >
        {languages.map((lang) => (
          <option key={lang.code} value={lang.code}>
            {lang.name}
          </option>
        ))}
      </Select>

      <IconButton
        aria-label="Swap Languages"
        icon={<RepeatIcon />}
        size="md"
        onClick={swapLanguages}
      />

      <Select
        value={targetLanguage}
        onChange={(e) => setTargetLanguage(e.target.value)}
      >
        {languages.map((lang) => (
          <option key={lang.code} value={lang.code}>
            {lang.name}
          </option>
        ))}
      </Select>
    </Flex>
  );
};

export default LanguageSelector;