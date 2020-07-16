import { createContext, useContext } from 'react';
import EditorStore from './editor';
import UserStores from './User';
import AuthStore from './Auth';

const context = createContext({
  EditorStore,
  UserStores,
  AuthStore
})

export const useStores = () => useContext(context)

Window.AuthStore = AuthStore