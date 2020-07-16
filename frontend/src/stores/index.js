import { createContext, useContext } from 'react';
import EditorStore from './editor';
import UserStore from './User';
import AuthStore from './Auth';

const context = createContext({
  EditorStore,
  UserStore,
  AuthStore
})

export const useStores = () => useContext(context)

Window.AuthStore = AuthStore
Window.UserStore = UserStore