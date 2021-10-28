import System.Environment

import Randomness

-- prior
type Guesser = IO Float

-- posterior
type Checker = Float -> [Int] -> IO Bool


obs :: [Int]
obs = [0, 0, 1, 0, 0]


guesser :: Guesser
guesser = uniform (0, 1)


checker :: Checker
checker p obs = do
    rs <- gen (length obs) p
    return (rs == obs)


infer :: Guesser -> Checker -> [Int] -> IO Float
infer g c o = do
    g' <- g
    r <- c g' o
    if r then return g' else infer g c o


inferN :: Int -> IO [Float]
inferN 0 = return []
inferN n = do
    x <- infer guesser checker obs
    xs <- inferN (n-1)
    return (x:xs)


main :: IO ()
main = do
    a <- getArgs
    xs <- inferN (read (head a) :: Int)
    mapM_ print xs
