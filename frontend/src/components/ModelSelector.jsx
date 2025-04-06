import React from 'react';
import { Select } from '@chakra-ui/react';

const ModelSelector = ({ model, setModel, models }) => {
  return (
    <Select
      value={model}
      onChange={(e) => setModel(e.target.value)}
      w="180px"
    >
      {models.map((model) => (
        <option key={model.id} value={model.id}>
          {model.name}
        </option>
      ))}
    </Select>
  );
};

export default ModelSelector;