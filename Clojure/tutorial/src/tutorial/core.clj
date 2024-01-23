(ns tutorial.core
  (:gen-class))

(defn example [] ; Example Function
  (println (str "Hello Mom!"))
  (println (* 3 2)) 

  #_{:clj-kondo/ignore [:inline-def]}
  (def x 1)
  #_{:clj-kondo/ignore [:inline-def]}
  (def y 2)

  (println (+ x y))
  (println  (inc x))
)


(defn -main [] ; Main Function
  (example)
  
  )