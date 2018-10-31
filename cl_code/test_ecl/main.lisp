
;(format t "test gcl [main.lisp]")

;(defvar *data* nil)
;(defvar *datafile* "00.txt")
;(defvar *tmp* nil)
;(defvar *tmp2* nil)


;(makunbound '*data*)
;(makunbound '*tmp*)
;(makunbound '*db*)

(defvar *data* nil)
(defvar *tmp* nil)
(defvar *db* nil)

(defvar *num-of-cells* nil)
(defvar *cells-list* nil)
(defvar *lines-pos* nil)
(defvar *cells-data* nil)
(defvar *cells-coord* nil)
(defvar *data-table* nil)
(defvar *cells-param* nil)

(defmacro x-set-global (varname value)
  `(list 'setf ,varname ,value)))

(defun x-load (filename)
  (let ((in (open filename)))
    (do ((line (read-line in) (read-line in)))
	((null line) (close in))
      (push line *data*))
    (setf *data* (reverse *data*))))

(defun x-load1-old (filename)
  (if (equal (length *data*) 0)
      (with-open-file (stream filename)
	(do ((line (read-line stream nil)
		   (read-line stream nil)))
	    ((null line))
	  (push line *data*)))
      (eval (x-set-global '*data* '(reverse *data*))))
  (return-from x-load1 nil)))

(defun x-load1 (filename)
  (with-open-file (stream filename)
    (do ((line (read-line stream nil)
	       (read-line stream nil)))
	((null line))
      (push line *data*)))
  (eval (x-set-global '*data* '(reverse *data*)))
  (return-from x-load1 nil))


(defun x-proc (data)
  (let ((tmp (reverse data)))
    (setf tmp (nth 1 tmp))
    (setf tmp (substitute #\SPACE #\; tmp))
    (setf tmp (concatenate 'string "(" tmp ")"))
    (setf tmp (read-from-string tmp))
    (setf *tmp* tmp)))

(defun x-proc1-old (data index)
  (let ((tmp data))
    (setf tmp (nth index tmp))
    (setf tmp (substitute #\SPACE #\; tmp))
    (setf tmp (substitute #\. #\, tmp))
    (setf tmp (concatenate 'string "(" tmp ")"))
    (setf tmp (read-from-string tmp))
    (push tmp *db*)
    nil))

(defun x-proc1 (data index)
  (let ((tmp data))
    (setf tmp (nth index tmp))
    (setf offset (position (string #\;) tmp :test #'string=))
    (setf tmp (subseq tmp offset (1- (length tmp))))
    (setf tmp (substitute #\SPACE #\; tmp))
    (setf tmp (substitute #\. #\, tmp))
    (setf tmp (concatenate 'string "(" tmp ")"))
    (setf tmp (read-from-string tmp))
    (if (not (equal (search "Параметер" (nth index data)) nil))
	(setf tmp
	      (loop for i from 0 below (- (length tmp) 1) by 2
		 collect (concatenate
			  'string
			  (string (nth i tmp))
			  " "
			  (string (nth (1+ i) tmp))))))
    (push tmp *db*)
    nil))

(defun x-proc2 (data start end)
  (do ((n start (1+ n)))
      ((= n end))
    (x-proc1 data n)))


	

(defun x-proc3 (data)
  (setf ind (loop for i from 0 upto (1- (length data)) collect i))
  (setf ind (remove-if-not #'(lambda (i) (or (equal (count #\; (nth i data)) 0)
					     (<= (length (nth i data)) 3) nil)) ind))
  (setf tmp-ind (eval (append (list 'map ''list '#'list)
			      (mapcar #'(lambda (x) `(quote ,x))
				      (map 'list #'eval
					   (loop for i in (list 'remove-if-not 'remove-if)
					      collect (append (list i) '(#'evenp ind))))))))
  (setf tmp-ind (mapcar #'(lambda (x) (list (1+ (car x)) (1- (nth 1 x)))) tmp-ind))
  (return-from x-proc3 tmp-ind))

(defun x-proc4-old (data ncells)
  (if (<= (length (nth 0 data)) 2) (setf data (reverse data)))
  (if (not (>= (length *db*) (* ncells 13)))
      ((setf ind (x-proc3 data))
       (setf cnames nil)
       (loop for i in ind do
	    (when
		(< (position i ind) ncells)
	      (x-proc2 data (car i) (nth 1 i))))
;      (push (nth (1- (car ind)) data) cnames)))
       (setf res nil)
       (setf k (car ind))
       (setf k (- (nth 1 k) (nth 0 k)))
       nil)))
;  (loop for i from 0 upto (- ncells 2) do
;       (push
;	(subseq *db* (* i k) (* (1+ i) k)) res))
;  (return-from x-proc4 (list cnames res)))

(defun x-proc4 (data ncells)
  (if (equal *lines-pos* nil) (setf ind (x-proc3 data)) (setf ind *lines-pos*))
  (setf cnames nil)
  (loop for i in ind do
       (when
	   (< (position i ind) ncells)
	 (x-proc2 data (car i) (nth 1 i))))
  (setf res nil)
  (setf k (car ind))
  (setf k (- (nth 1 k) (nth 0 k)))
  nil)

(defun x-proc5 (db data nl)
  (if (equal nl 0) (setf nl (eval `(- (- ,@(car *lines-pos*))))))
  (setf n (length db))
  (setf m (1- (/ n nl)))
  (setf res nil)
  (setf cnames nil)
  (loop for i from 0 upto m do
       (push (reverse (subseq db (* i nl) (* (1+ i) nl))) res))
  (loop for i from 0 upto m do
       (push (nth (* i (+ nl 3)) data) cnames))
  (return-from x-proc5 (list cnames res)))

(defun x-show-db (db n m)
  (if (equal m 0) (setf m (1- (length db)))) 
  (mapcar
   #'(lambda (x)
       (format t "~a~%" (subseq x 0 (if (equal n 0) (1- (length x))))))
   (subseq db 0 m)))

(defun x-show-db2 (p n m)
  (if (equal m 0) (setf m (1- (length (nth 1 p)))))
  (loop for i in (nth 1 p) do
       (when
	   (not (format t "~a~%" (nth (position i (nth 1 p)) (nth 0 p))))
	 (mapcar
	  #'(lambda (x)
	      (format t "~t~a~%" (subseq x 0 (if (equal n 0) (1- (length x)))))) i))))



(defun x-cell-list (data)
  (setf cell-list nil)
  (setf offset (1+ (position (string #\Return) data :test #'string=)))
  (loop for i from 0 upto (1- (/ (length data) offset)) do
       (push (nth (* i offset) data) cell-list))
  (return-from x-cell-list (reverse cell-list)))

(defun x-mean (x)
  (return-from x-mean (/ (reduce #'+ x) (length x))))

(defun x-disp (x)
  (setf m (x-mean x))
  (return-from x-disp (/ (reduce #'+ (mapcar #'(lambda (x) (expt (- x m) 2)) b)) length(x))))

(defun x-mean0 (x)
  (setf m (x-mean x))
  (return-from x-mean0 (mapcar #'(lambda (x) (- x m)) x)))

(defun x-std (x)
  (setf std2 (x-disp x))
  (return-from x-std (expt std2 0.5)))



(defun x-get-cell-coords (cell-list)
  (if (equal cell-list nil) (setf cell-list *cells-list*))
  (setf res (mapcar
	     #'(lambda (x)
		 (concatenate
		  'string
		  ":"
		  (string (second (read-from-string
				   (concatenate 'string "(" x ")")))))) cell-list))
  (return-from x-get-cell-coords res))


(defun x-show-cells (cell-list)
  (if (equal cell-list nil) (setf cell-list *cells-list*))
  (format t "~{~a~%~}~%" cell-list))


(defun x-show-all-cells-data (cell-coord cell-data)
  (if (equal cell-coord nil) (setf cell-coord *cells-coord*))
  (if (equal cell-data nil) (setf cell-data *cells-data*))
  (setf cell-info nil)
  (setf cell-info (mapcar
   #'(lambda (x)
       `(,(read-from-string (car x)) ,@(cdr x)))
   (map 'list #'list cell-coord cell-data)))
  (setf cell-info
	(eval `(append
		,@(loop for i in cell-info collect `(quote ,i)))))
;  (setf cell-info (eval `(append ,@cell-info)))  
  (return-from x-show-all-cells-data cell-info))

(defun x-print-table (dt cells)
  (setf all-cells
	(mapcar
	 #'(lambda (x)
	     (concatenate
	      'string
	      (cdr (loop for i across x collect i))))
	 *cells-coord*))
  (if (equal cells nil) (setf cells all-cells))
  (if (equal dt nil) (setf dt *data-table*))
  (setf tmp-dt (map 'list #'list (mapcar #'string (remove-if #'listp dt)) (remove-if-not #'listp dt)))
;  (setf tmp-dt (reduce #'nconc (loop for (i j) in tmp-dt when (find i cells :test #'string=) collect (list i j))))
    (setf tmp-dt (loop for (i j) in tmp-dt when (find i cells :test #'string=) collect (list i j)))
;(return-from x-print-table tmp-dt))
    (loop for i in tmp-dt do
      (when T
	 (format t "CELL: ~a~%" (first i))
	 (format t "~{~8t~a~%~}~%" (second i)))))
;  (when T
;	(setf target-data (mapcar #'(lambda (x) (eval `(getf dt ,x))) cells))
;	(setf dt (remove-if #'(lambda (x) (equal (position x target-data) nil)) dt))
;	(setf dt (remove-if #'(lambda (x) (equal (position x cells) nil)) dt))))
 ; (format t "~{CELL: ~a~%~{~8t~a~%~}~}~%" dt))

;(defvar *num-of-cells* nil)
;(defvar *cells-list* nil)
;(defvar *lines-pos* nil)


(defun x-get-rows-names ()
  (setf res
	(loop for
	   i from (caar *lines-pos*)
	   upto (cadar *lines-pos*)
	   collect
	     (subseq (nth i *data*) 0
		     (position (string #\;) (nth i *data*) :test #'string=))))
  (return-from x-get-rows-names
    (mapcar #'(lambda (x) (string-trim '(#\SPACE #\TAB #\NEWLINE) x)) res)))



(defun x-main () 
  (if (equal *data* nil) (x-load1 "00.txt"))
  (if (equal *cells-list* nil) (setf *cells-list* (x-cell-list *data*)))
  (if (equal *num-of-cells* nil) (setf *num-of-cells* (length *cells-list*)))
  (if (equal *lines-pos* nil) (setf *lines-pos* (x-proc3 *data*)))
  (if (equal *db* nil) (x-proc4 *data* *num-of-cells*))
  (if (equal *cells-data* nil) (setf *cells-data* (nth 1 (x-proc5 *db* *data* 0))))
  (if (equal *cells-coord* nil) (setf *cells-coord* (x-get-cell-coords *cells-list*)))
  (if (equal *data-table* nil) (setf *data-table* (x-show-all-cells-data nil nil)))
  (if (equal *cells-param* nil) (setf *cells-param* (x-get-rows-names)))
  nil)



;(x-load "00.txt")

(setf tmp-cmd `(when (load "main.lisp") (x-load1 "00.txt")))


(defun a-offset (a b c d) (/ (- (+ a b) (+ c d)) (+ a b c d)))

;(x-load1 "00.txt")
;(x-proc4 *data* 48)
;(setf data (x-proc5 *db* *data* 13))

(defun x-test (data cnt)
;  (setf d0 (second (reverse (getf *data-table* :30-41))))
  (setf tmp-data (nth cnt data))
  (setf tmp-data (mapcar #'(lambda (x) (format nil "~a " x)) tmp-data))
  (setf tmp-data
	(loop for i from 0 upto (- (/ (length tmp-data) 4) 1)
	   collect (subseq tmp-data (* i 4) (* (+ i 1) 4))))
  (setf tmp-data (mapcar #'(lambda (x) (eval `(concatenate 'string ,@x))) tmp-data))
  (setf tmp-data
	(mapcar
	 #'(lambda (x) (substitute #\) #\} x))
	 (mapcar
	  #'(lambda (x) (substitute #\( #\{ x)) tmp-data)))
;  (return-from x-test tmp-data))
  (setf tmp-data (map 'list #'read-from-string tmp-data))
  (return-from x-test tmp-data))

(defun x-test2 (db)
  (if (equal db nil) (setf db *db*))
  (setf res nil)
  (loop for x in db do
       (if
	(and (equal (type-of (car x)) 'symbol)
	     (not (equal (search "{" (string (car x))) nil)) T)
	 (push (x-test
		db
		(position x db))
	       res)
	 (push x res)))
  (return-from x-test2 (reverse res)))
			   

(defun x-test3 (db)
  (setf tmp-data (x-test2 db))
  (setf *data-table* nil)
  (setf *cells-data* nil)
  (setf *db* tmp-data)
  (x-main)
  nil)

(defun x-proc-rows (data)
  (setf res
	(loop for i in data collect
	     (remove-if
	      #'(lambda (x)
		  (and
		   (equal (type-of x) 'symbol)
		   (not (string= x "[нет]"))
		   T)) i)))
  (return-from x-proc-rows res))

(defun x-proc-rows2 ()
  (setf res
	'("param" "zagr" "W" "G" "suz" "w" "Wt" "dkr1" "dkr2" "dkr1s" "dkr2s" "dkv1" "dkv2" "zapas"))
  (return-from x-proc-rows2 res))

(defun x-make-table (data head nc nr)
;  (if (equal head nil) (setf head *cells-param*))
  (if (equal head nil) (setf head (x-proc-rows2)))
  (setf tmp-data
	(loop for k from 0 below (1- (length (car data))) by 1
	   collect (mapcar #'(lambda (x) (nth k x)) data)))
  (if (not (equal nc nil))
      (when
	  (setf tmp-data (mapcar #'(lambda (x) (subseq x (car nc) (second nc))) tmp-data))
      (if (equal (type-of head) 'cons) (setf head (subseq head (car nc) (second nc))))))
  (if (not (equal nr nil)) (setf tmp-data (subseq tmp-data (car nr) (second nr))))
  (if (equal head T) (setf tmp-table tmp-data) (setf tmp-table (cons head tmp-data)))
  (format t "~{  ~a ~t ~t ~} ~%" head)
  (format t "~{ ~{ ~15@A ~} ~% ~}"
	  tmp-data))