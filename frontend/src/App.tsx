import './App.css'

// Redux
import { reduxStore } from './redux';
import { Provider as ReduxProvider } from 'react-redux';

import Main from './pages/Main';

export default () => {

  return <ReduxProvider store={reduxStore}>
    <Main />
  </ReduxProvider>
}


