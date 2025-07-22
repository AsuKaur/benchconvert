(set-logic QF_BVFP)
(declare-fun X_0 () (_ FloatingPoint 8 24))
(declare-fun X_1 () (_ FloatingPoint 8 24))
(declare-fun X_2 () (_ FloatingPoint 8 24))
(declare-fun X_3 () (_ FloatingPoint 8 24))
(assert (fp.leq X_0 (fp #b0 #x7f #b00000000000000000000000)))
(assert (fp.geq X_0 (_ +zero 8 24)))
(assert (fp.leq X_1 (fp #b0 #x7f #b00000000000000000000000)))
(assert (fp.geq X_1 (_ +zero 8 24)))
(assert (fp.leq X_2 (fp #b0 #x7f #b00000000000000000000000)))
(assert (fp.geq X_2 (_ +zero 8 24)))
(assert (fp.leq X_3 (fp #b0 #x7f #b00000000000000000000000)))
(assert (fp.geq X_3 (_ +zero 8 24)))
(declare-fun H_0_0 () (_ FloatingPoint 8 24))
(declare-fun H_0_1 () (_ FloatingPoint 8 24))
(declare-fun H_0_2 () (_ FloatingPoint 8 24))
(declare-fun H_0_3 () (_ FloatingPoint 8 24))
(declare-fun H_0_4 () (_ FloatingPoint 8 24))
(declare-fun H_0_5 () (_ FloatingPoint 8 24))
(declare-fun H_0_6 () (_ FloatingPoint 8 24))
(declare-fun H_0_7 () (_ FloatingPoint 8 24))
(declare-fun H_0_8 () (_ FloatingPoint 8 24))
(declare-fun H_0_9 () (_ FloatingPoint 8 24))
(declare-fun H_0_10 () (_ FloatingPoint 8 24))
(declare-fun H_0_11 () (_ FloatingPoint 8 24))
(declare-fun H_0_12 () (_ FloatingPoint 8 24))
(declare-fun H_0_13 () (_ FloatingPoint 8 24))
(declare-fun H_0_14 () (_ FloatingPoint 8 24))
(declare-fun H_0_15 () (_ FloatingPoint 8 24))
(assert (= H_0_0 (let ((a!1 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   (_ +zero 8 24)
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b0 #x7f #b00000000000000000000000)
                                           X_0))
                           (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_1))
                   (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_2))))
  (fp.add roundNearestTiesToEven
          a!1
          (fp.mul roundNearestTiesToEven
                  (fp #b1 #x7f #b00000000000000000000000)
                  X_3)))))
(assert (= H_0_1 (let ((a!1 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   (_ +zero 8 24)
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b1 #x7f #b00000000000000000000000)
                                           X_0))
                           (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_1))
                   (fp.mul roundNearestTiesToEven
                           (fp #b0 #x7f #b00000000000000000000000)
                           X_2))))
  (fp.add roundNearestTiesToEven
          a!1
          (fp.mul roundNearestTiesToEven
                  (fp #b1 #x7f #b00000000000000000000000)
                  X_3)))))
(assert (= H_0_2 (let ((a!1 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   (fp #b1 #x80 #b00000000000000000000000)
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b1 #x7f #b00000000000000000000000)
                                           X_0))
                           (fp.mul roundNearestTiesToEven
                                   (fp #b0 #x7f #b00000000000000000000000)
                                   X_1))
                   (fp.mul roundNearestTiesToEven
                           (fp #b0 #x7f #b00000000000000000000000)
                           X_2))))
  (fp.add roundNearestTiesToEven
          a!1
          (fp.mul roundNearestTiesToEven
                  (fp #b0 #x7f #b00000000000000000000000)
                  X_3)))))
(assert (= H_0_3 (let ((a!1 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   (fp #b0 #x7f #b00000000000000000000000)
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b1 #x7f #b00000000000000000000000)
                                           X_0))
                           (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_1))
                   (fp.mul roundNearestTiesToEven
                           (fp #b1 #x7f #b00000000000000000000000)
                           X_2))))
  (fp.add roundNearestTiesToEven
          a!1
          (fp.mul roundNearestTiesToEven
                  (fp #b1 #x7f #b00000000000000000000000)
                  X_3)))))
(assert (= H_0_4 (let ((a!1 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   (fp #b1 #x80 #b00000000000000000000000)
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b0 #x7f #b00000000000000000000000)
                                           X_0))
                           (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_1))
                   (fp.mul roundNearestTiesToEven
                           (fp #b0 #x7f #b00000000000000000000000)
                           X_2))))
  (fp.add roundNearestTiesToEven
          a!1
          (fp.mul roundNearestTiesToEven
                  (fp #b0 #x7f #b00000000000000000000000)
                  X_3)))))
(assert (= H_0_5 (let ((a!1 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   (fp #b1 #x7f #b00000000000000000000000)
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b0 #x7f #b00000000000000000000000)
                                           X_0))
                           (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_1))
                   (fp.mul roundNearestTiesToEven
                           (fp #b1 #x7f #b00000000000000000000000)
                           X_2))))
  (fp.add roundNearestTiesToEven
          a!1
          (fp.mul roundNearestTiesToEven
                  (fp #b0 #x7f #b00000000000000000000000)
                  X_3)))))
(assert (= H_0_6 (let ((a!1 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   (fp #b1 #x7f #b00000000000000000000000)
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b1 #x7f #b00000000000000000000000)
                                           X_0))
                           (fp.mul roundNearestTiesToEven
                                   (fp #b0 #x7f #b00000000000000000000000)
                                   X_1))
                   (fp.mul roundNearestTiesToEven
                           (fp #b1 #x7f #b00000000000000000000000)
                           X_2))))
  (fp.add roundNearestTiesToEven
          a!1
          (fp.mul roundNearestTiesToEven
                  (fp #b0 #x7f #b00000000000000000000000)
                  X_3)))))
(assert (= H_0_7 (let ((a!1 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   (_ +zero 8 24)
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b1 #x7f #b00000000000000000000000)
                                           X_0))
                           (fp.mul roundNearestTiesToEven
                                   (fp #b1 #x7f #b00000000000000000000000)
                                   X_1))
                   (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_2))))
  (fp.add roundNearestTiesToEven
          a!1
          (fp.mul roundNearestTiesToEven
                  (fp #b0 #x7f #b00000000000000000000000)
                  X_3)))))
(assert (= H_0_8 (let ((a!1 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   (_ +zero 8 24)
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b0 #x7f #b00000000000000000000000)
                                           X_0))
                           (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_1))
                   (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_2))))
  (fp.add roundNearestTiesToEven
          a!1
          (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_3)))))
(assert (= H_0_9 (let ((a!1 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   (_ +zero 8 24)
                                   (fp.mul roundNearestTiesToEven
                                           (_ +zero 8 24)
                                           X_0))
                           (fp.mul roundNearestTiesToEven
                                   (fp #b0 #x7f #b00000000000000000000000)
                                   X_1))
                   (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_2))))
  (fp.add roundNearestTiesToEven
          a!1
          (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_3)))))
(assert (= H_0_10 (let ((a!1 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   (_ +zero 8 24)
                                   (fp.mul roundNearestTiesToEven
                                           (_ +zero 8 24)
                                           X_0))
                           (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_1))
                   (fp.mul roundNearestTiesToEven
                           (fp #b0 #x7f #b00000000000000000000000)
                           X_2))))
  (fp.add roundNearestTiesToEven
          a!1
          (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_3)))))
(assert (= H_0_11 (let ((a!1 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   (_ +zero 8 24)
                                   (fp.mul roundNearestTiesToEven
                                           (_ +zero 8 24)
                                           X_0))
                           (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_1))
                   (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_2))))
  (fp.add roundNearestTiesToEven
          a!1
          (fp.mul roundNearestTiesToEven
                  (fp #b0 #x7f #b00000000000000000000000)
                  X_3)))))
(assert (= H_0_12 (let ((a!1 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   (fp #b1 #x7f #b00000000000000000000000)
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b0 #x80 #b00000000000000000000000)
                                           X_0))
                           (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_1))
                   (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_2))))
  (fp.add roundNearestTiesToEven
          a!1
          (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_3)))))
(assert (= H_0_13 (let ((a!1 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   (fp #b1 #x7f #b00000000000000000000000)
                                   (fp.mul roundNearestTiesToEven
                                           (_ +zero 8 24)
                                           X_0))
                           (fp.mul roundNearestTiesToEven
                                   (fp #b0 #x80 #b00000000000000000000000)
                                   X_1))
                   (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_2))))
  (fp.add roundNearestTiesToEven
          a!1
          (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_3)))))
(assert (= H_0_14 (let ((a!1 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   (fp #b1 #x7f #b00000000000000000000000)
                                   (fp.mul roundNearestTiesToEven
                                           (_ +zero 8 24)
                                           X_0))
                           (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_1))
                   (fp.mul roundNearestTiesToEven
                           (fp #b0 #x80 #b00000000000000000000000)
                           X_2))))
  (fp.add roundNearestTiesToEven
          a!1
          (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_3)))))
(assert (= H_0_15 (let ((a!1 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   (fp #b1 #x7f #b00000000000000000000000)
                                   (fp.mul roundNearestTiesToEven
                                           (_ +zero 8 24)
                                           X_0))
                           (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_1))
                   (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_2))))
  (fp.add roundNearestTiesToEven
          a!1
          (fp.mul roundNearestTiesToEven
                  (fp #b0 #x80 #b00000000000000000000000)
                  X_3)))))
(declare-fun H_1_0 () (_ FloatingPoint 8 24))
(declare-fun H_1_1 () (_ FloatingPoint 8 24))
(declare-fun H_1_2 () (_ FloatingPoint 8 24))
(declare-fun H_1_3 () (_ FloatingPoint 8 24))
(declare-fun H_1_4 () (_ FloatingPoint 8 24))
(declare-fun H_1_5 () (_ FloatingPoint 8 24))
(declare-fun H_1_6 () (_ FloatingPoint 8 24))
(declare-fun H_1_7 () (_ FloatingPoint 8 24))
(declare-fun H_1_8 () (_ FloatingPoint 8 24))
(declare-fun H_1_9 () (_ FloatingPoint 8 24))
(declare-fun H_1_10 () (_ FloatingPoint 8 24))
(declare-fun H_1_11 () (_ FloatingPoint 8 24))
(declare-fun H_1_12 () (_ FloatingPoint 8 24))
(declare-fun H_1_13 () (_ FloatingPoint 8 24))
(declare-fun H_1_14 () (_ FloatingPoint 8 24))
(declare-fun H_1_15 () (_ FloatingPoint 8 24))
(assert (= H_1_0 (ite (fp.geq H_0_0 (_ +zero 8 24)) H_0_0 (_ +zero 8 24))))
(assert (= H_1_1 (ite (fp.geq H_0_1 (_ +zero 8 24)) H_0_1 (_ +zero 8 24))))
(assert (= H_1_2 (ite (fp.geq H_0_2 (_ +zero 8 24)) H_0_2 (_ +zero 8 24))))
(assert (= H_1_3 (ite (fp.geq H_0_3 (_ +zero 8 24)) H_0_3 (_ +zero 8 24))))
(assert (= H_1_4 (ite (fp.geq H_0_4 (_ +zero 8 24)) H_0_4 (_ +zero 8 24))))
(assert (= H_1_5 (ite (fp.geq H_0_5 (_ +zero 8 24)) H_0_5 (_ +zero 8 24))))
(assert (= H_1_6 (ite (fp.geq H_0_6 (_ +zero 8 24)) H_0_6 (_ +zero 8 24))))
(assert (= H_1_7 (ite (fp.geq H_0_7 (_ +zero 8 24)) H_0_7 (_ +zero 8 24))))
(assert (= H_1_8 (ite (fp.geq H_0_8 (_ +zero 8 24)) H_0_8 (_ +zero 8 24))))
(assert (= H_1_9 (ite (fp.geq H_0_9 (_ +zero 8 24)) H_0_9 (_ +zero 8 24))))
(assert (= H_1_10 (ite (fp.geq H_0_10 (_ +zero 8 24)) H_0_10 (_ +zero 8 24))))
(assert (= H_1_11 (ite (fp.geq H_0_11 (_ +zero 8 24)) H_0_11 (_ +zero 8 24))))
(assert (= H_1_12 (ite (fp.geq H_0_12 (_ +zero 8 24)) H_0_12 (_ +zero 8 24))))
(assert (= H_1_13 (ite (fp.geq H_0_13 (_ +zero 8 24)) H_0_13 (_ +zero 8 24))))
(assert (= H_1_14 (ite (fp.geq H_0_14 (_ +zero 8 24)) H_0_14 (_ +zero 8 24))))
(assert (= H_1_15 (ite (fp.geq H_0_15 (_ +zero 8 24)) H_0_15 (_ +zero 8 24))))
(declare-fun H_2_0 () (_ FloatingPoint 8 24))
(declare-fun H_2_1 () (_ FloatingPoint 8 24))
(assert (= H_2_0 (let ((a!1 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   (fp #b0 #x7f #b00000000000000000000000)
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b1 #x7f #b00000000000000000000000)
                                           H_1_0))
                           (fp.mul roundNearestTiesToEven
                                   (fp #b1 #x7f #b00000000000000000000000)
                                   H_1_1))
                   (fp.mul roundNearestTiesToEven
                           (fp #b1 #x7f #b00000000000000000000000)
                           H_1_2))))
(let ((a!2 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   a!1
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b1 #x7f #b00000000000000000000000)
                                           H_1_3))
                           (fp.mul roundNearestTiesToEven
                                   (fp #b1 #x7f #b00000000000000000000000)
                                   H_1_4))
                   (fp.mul roundNearestTiesToEven
                           (fp #b1 #x7f #b00000000000000000000000)
                           H_1_5))))
(let ((a!3 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   a!2
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b1 #x7f #b00000000000000000000000)
                                           H_1_6))
                           (fp.mul roundNearestTiesToEven
                                   (fp #b1 #x7f #b00000000000000000000000)
                                   H_1_7))
                   (fp.mul roundNearestTiesToEven (_ +zero 8 24) H_1_8))))
(let ((a!4 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   a!3
                                   (fp.mul roundNearestTiesToEven
                                           (_ +zero 8 24)
                                           H_1_9))
                           (fp.mul roundNearestTiesToEven (_ +zero 8 24) H_1_10))
                   (fp.mul roundNearestTiesToEven (_ +zero 8 24) H_1_11))))
(let ((a!5 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   a!4
                                   (fp.mul roundNearestTiesToEven
                                           (_ +zero 8 24)
                                           H_1_12))
                           (fp.mul roundNearestTiesToEven (_ +zero 8 24) H_1_13))
                   (fp.mul roundNearestTiesToEven (_ +zero 8 24) H_1_14))))
  (fp.add roundNearestTiesToEven
          a!5
          (fp.mul roundNearestTiesToEven (_ +zero 8 24) H_1_15)))))))))
(assert (= H_2_1 (let ((a!1 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   (_ +zero 8 24)
                                   (fp.mul roundNearestTiesToEven
                                           (_ +zero 8 24)
                                           H_1_0))
                           (fp.mul roundNearestTiesToEven (_ +zero 8 24) H_1_1))
                   (fp.mul roundNearestTiesToEven (_ +zero 8 24) H_1_2))))
(let ((a!2 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   a!1
                                   (fp.mul roundNearestTiesToEven
                                           (_ +zero 8 24)
                                           H_1_3))
                           (fp.mul roundNearestTiesToEven (_ +zero 8 24) H_1_4))
                   (fp.mul roundNearestTiesToEven (_ +zero 8 24) H_1_5))))
(let ((a!3 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   a!2
                                   (fp.mul roundNearestTiesToEven
                                           (_ +zero 8 24)
                                           H_1_6))
                           (fp.mul roundNearestTiesToEven (_ +zero 8 24) H_1_7))
                   (fp.mul roundNearestTiesToEven
                           (fp #b0 #x7f #b00000000000000000000000)
                           H_1_8))))
(let ((a!4 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   a!3
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b0 #x7f #b00000000000000000000000)
                                           H_1_9))
                           (fp.mul roundNearestTiesToEven
                                   (fp #b0 #x7f #b00000000000000000000000)
                                   H_1_10))
                   (fp.mul roundNearestTiesToEven
                           (fp #b0 #x7f #b00000000000000000000000)
                           H_1_11))))
(let ((a!5 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   a!4
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b1 #x7f #b00000000000000000000000)
                                           H_1_12))
                           (fp.mul roundNearestTiesToEven
                                   (fp #b1 #x7f #b00000000000000000000000)
                                   H_1_13))
                   (fp.mul roundNearestTiesToEven
                           (fp #b1 #x7f #b00000000000000000000000)
                           H_1_14))))
  (fp.add roundNearestTiesToEven
          a!5
          (fp.mul roundNearestTiesToEven
                  (fp #b1 #x7f #b00000000000000000000000)
                  H_1_15)))))))))
(declare-fun Y_0 () (_ FloatingPoint 8 24))
(assert (= Y_0 H_2_0))
(declare-fun Y_1 () (_ FloatingPoint 8 24))
(assert (= Y_1 H_2_1))
(assert (fp.geq Y_0 (fp #b0 #x7f #b00000000000000000000000)))
(assert (fp.leq Y_1 (_ +zero 8 24)))
(check-sat)
(get-model)