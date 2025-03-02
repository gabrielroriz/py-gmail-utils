import './App.css'

// Redux
import { reduxStore } from './redux';
import { Provider as ReduxProvider } from 'react-redux';

import Main from './pages/Main';

// Tauri
import { invoke } from '@tauri-apps/api'

export default () => {

  invoke('greet', { name: 'World' })

  return <ReduxProvider store={reduxStore}>
    <Main />
  </ReduxProvider>
}


