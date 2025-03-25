import React from 'react';
import { Textarea, Box } from '@chakra-ui/react';

const TranslationTextarea = ({
  value,
  onChange,
  placeholder,
  isReadOnly = false,
}) => {
  return (
    <Box flex={1} position="relative">
      <Textarea
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        size="lg"
        height="250px"
        fontSize="lg"
        isReadOnly={isReadOnly}
      />
    </Box>
  );
};

export default TranslationTextarea;