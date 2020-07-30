import { createContext, useContext } from 'react';
import EditorStore from './editor';
import UserStore from './User';
import AuthStore from './Auth';
import PostStore from './Post';
import CategroyStory from './categroy';

const context = createContext({
  EditorStore,
  UserStore,
  AuthStore,
  PostStore,
  CategroyStory
})

export const useStores = () => useContext(context)

Window.AuthStore = AuthStore
Window.UserStore = UserStore
Window.PostStore = PostStore