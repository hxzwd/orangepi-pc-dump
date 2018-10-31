

(defvar *cell* "34-33")

(defvar *info-path* "NEWDATA/INFO")
(defvar *db* nil)

(defvar *info-list* (directory (concatenate 'string *info-path* "/*")))

(defvar *data-path* "NEWDATA")

(defvar *data-dirs*  (directory (concatenate 'string *data-path* "/*")))
(setf *data-dirs* (mapcar #'namestring *data-dirs*))
(setf *data-dirs* (remove-if #'(lambda (x) (search "INFO" x)) *data-dirs*))
;;#'(lambda (x) ((search "INFO" (namestring x))))
		



(defun f-get-fn (filename)
  (setf res nil)
  (with-open-file (stream filename)
    (do ((line (read-line stream nil)
	       (read-line stream nil))
	 (n 0 (1+ n)))
	((null line))
      (if (not (equal (search *cell* line) nil))
	  (setf res (list line n)))))
  (return-from f-get-fn res))



(defun f-get-data (filename)
  (setf res nil)
  (with-open-file (stream filename)
    (do ((line (read-line stream nil)
	       (read-line stream nil)))
	 ((null line))
	 (push line res)))
  (push (reverse res) *db*)
  nil)





(defvar *tmp* (mapcar #'f-get-fn *info-list*))

(setf tmp1 (mapcar #'(lambda (x)
		       (concatenate 'string "new"
				    (car (last (pathname-directory x)))))
		   *data-dirs*))

(setf tmp2 (mapcar #'(lambda (x)
		       (format nil "~2,'0d" x))
		   (mapcar #'(lambda (x) (nth 1 x)) *tmp*)))
(setf tmp3 (map 'list #'(lambda (x y z) (concatenate 'string (concatenate 'string z x) "_" y)) tmp1 tmp2 *data-dirs*))


(defun f-test (var)
  (mapcar #'f-get-data var))
