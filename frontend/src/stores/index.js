import { createContext, useContext } from 'react';
import EditorStore from './editor';

const context = createContext({
  EditorStore
})

export const useStores = () => useContext(context)