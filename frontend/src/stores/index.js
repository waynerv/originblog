import { createContext, useContext } from 'react';
import ListStore from './List'

const context = createContext({
  ListStore
})

export const useStores = () => useContext(context)