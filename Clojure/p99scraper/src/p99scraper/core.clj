(ns p99scraper.core
  (:gen-class)
  (:require [net.cgrand.enlive-html :as html]))
(require '[clojure.edn :as edn])
(def config (edn/read-string (slurp "config.edn")))
(def system-path (:system-path config))
(def output-path (:output-path config))

(defn read-html-file
  [file-path]
  (slurp file-path)) ; Reads the entire HTML file

(defn get-dom-from-file
  [file-path]
  (html/html-resource (java.io.StringReader. (read-html-file file-path)))) ; Parses HTML from the file

(defn extract-titles
  [dom]
  (html/select dom [[:h3.sz-session__title]])) ; Extract all <h3> elements with class sz-session__title

(defn extract-speakers
  [dom]
  (html/select dom [[:a]])) ; Extract all <a> elements (you might want a more specific selector here)

(defn write-items-to-file
  [file-path items]
  (spit file-path items)) ; Write the items to the specified file

(defn print-items
  [dom file-path]
  (let [titles (extract-titles dom) ; Get all titles
        speakers (extract-speakers dom) ; Get all speakers
        output (StringBuilder.)] ; Create a StringBuilder to accumulate output
    (doseq [i (range (count titles))] ; Iterate over the indices of titles
      (let [title (html/text (nth titles i)) ; Get the title at index i
            speaker (if (pos? i) (html/text (nth speakers (dec i))) "No Speaker")] ; Get the speaker at index i-1 or "No Speaker" for the first title
        (.append output (str title "," speaker "\n")))) ; Append each line to the output
    (write-items-to-file file-path (.toString output)))) ; Write the accumulated output to the specified file

(defn -main
  []
  (let [file-path system-path
        output-file output-path ; Specify the output file path
        dom (get-dom-from-file file-path)]
    (print-items dom output-file))) ; Call print-items to print the extracted items to the output file
