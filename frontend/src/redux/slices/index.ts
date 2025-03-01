import counterSlice from './counter';

export type ReduxRootState = {
    [counterSlice.name]: ReturnType<typeof counterSlice.reducer>;
};

export default [
    counterSlice,
]