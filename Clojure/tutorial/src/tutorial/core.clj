(ns tutorial.core
  (:gen-class))

(defn example [] ; Example Function
  (println (str "Hello Mom!"))
  (println (* 3 2))

  (let [x 1
        y 2]
    (println (+ x y))
    (println (inc x)))
  )

(defn arity  ; Loop function
  ([num] (println (+ num 2)))
  ([] (println (+ 1 2))))

(defn -main [] ; Main Function
  (example)
  (arity 6)
  (arity))