import React from 'react';
import { Button, Flex } from '@chakra-ui/react';
import { ArrowRightIcon } from '@chakra-ui/icons';

const TranslateButton = ({ onClick }) => {
  return (
    <Flex justify="center" mt={6}>
      <Button
        size="lg"
        colorScheme="blue"
        borderRadius="md"
        rightIcon={<ArrowRightIcon />}
        onClick={onClick}
      >
        Translate
      </Button>
    </Flex>
  );
};

export default TranslateButton;