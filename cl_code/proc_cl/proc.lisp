
(defvar *input-file* "/home/hjk/dump_dir/arc_data/arc1_txt_part/00.txt")
(defvar *db* nil)
(defvar *g-tmp* nil)

(defvar *data-path* (directory-namestring *input-file*))

(defun f-load (fn)
  (with-open-file (stream fn)
    (do ((line (read-line stream nil)
	       (read-line stream nil)))
	((null line))
      (push line *db*)))
  (setf *db* (reverse *db*))
  nil)

(defun f-load-2 (fn)
  (let ((in (open fn)))
    (do ((n 0 (1+ n)))
	((= n 767) (close in))
      (push (read-line in) *g-tmp*)))
  nil)

(defun f-load-3 (fn)
  (setf *g-tmp*
	(with-open-file (stream fn)
	  (loop for line = (read-line stream nil)
	     while line
	     collect line)))
  nil)

(defun f-load-4 (fn out)
  (with-output-to-string (out)
    (with-open-file (in fn)
      (loop with buffer = (make-array (* 64 (expt 2 20)) :element-type 'character)
	 for n-characters = (read-sequence buffer in)
	 while (< 0 n-characters)
	 do (write-sequence buffer out :start 0 :end n-characters)))))

(defun f-list-dir (dirn)
  (directory (concatenate 'string dirn "*.*")))

(defun f-print-list-dir (dirn)
  (format t "~%~a~% ~{~4t~a~%~}"
	  dirn
	  (mapcar 'file-namestring (f-list-dir dirn))))

