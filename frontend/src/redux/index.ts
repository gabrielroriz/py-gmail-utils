// Redux Config
import { configureStore } from '@reduxjs/toolkit';
import type { ReducersMapObject } from '@reduxjs/toolkit';

// Redux Slices
import reduxSlices, { ReduxRootState } from "./slices";

// Redux Hooks
import { useDispatch, useSelector } from 'react-redux';

/**
 * Reducers
 */
const reduxReducers: ReducersMapObject<ReduxRootState> = reduxSlices.reduce(
    (acc, slice) => ({
        ...acc,
        [slice.name]: slice.reducer
    }),
    {} as ReducersMapObject<ReduxRootState>
);

/**
 * Store
 */
export const reduxStore = configureStore({
    reducer: reduxReducers,
    devTools: process.env.NODE_ENV !== 'production'
});

/**
 * Actions
 */
export type ReduxActions = {
    [K in (typeof reduxSlices)[number]['name']]: Extract<
        (typeof reduxSlices)[number],
        { name: K }
    >['actions'];
};

export const reduxActions = reduxSlices.reduce(
    (acc, slice) => ({
        ...acc,
        [slice.name]: slice.actions
    }),
    {} as ReduxActions
);

/**
 * Hooks
 */
export const useReduxSelector = useSelector.withTypes<ReduxRootState>();

export const useReduxDispatch = useDispatch.withTypes<typeof reduxStore.dispatch>();