(set-logic QF_BVFP)
(declare-fun X_0 () (_ FloatingPoint 8 24))
(declare-fun X_1 () (_ FloatingPoint 8 24))
(declare-fun X_2 () (_ FloatingPoint 8 24))
(declare-fun X_3 () (_ FloatingPoint 8 24))
(declare-fun X_4 () (_ FloatingPoint 8 24))
(declare-fun X_5 () (_ FloatingPoint 8 24))
(declare-fun X_6 () (_ FloatingPoint 8 24))
(assert (fp.leq X_0 (fp #b0 #x7f #b00000000000000000000000)))
(assert (fp.geq X_0 (_ +zero 8 24)))
(assert (fp.leq X_1 (fp #b0 #x7f #b00000000000000000000000)))
(assert (fp.geq X_1 (_ +zero 8 24)))
(assert (fp.leq X_2 (fp #b0 #x7f #b00000000000000000000000)))
(assert (fp.geq X_2 (_ +zero 8 24)))
(assert (fp.leq X_3 (fp #b0 #x7f #b00000000000000000000000)))
(assert (fp.geq X_3 (_ +zero 8 24)))
(assert (fp.leq X_4 (fp #b0 #x7f #b00000000000000000000000)))
(assert (fp.geq X_4 (_ +zero 8 24)))
(assert (fp.leq X_5 (fp #b0 #x7f #b00000000000000000000000)))
(assert (fp.geq X_5 (_ +zero 8 24)))
(assert (fp.leq X_6 (fp #b0 #x7f #b00000000000000000000000)))
(assert (fp.geq X_6 (_ +zero 8 24)))
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
(declare-fun H_0_16 () (_ FloatingPoint 8 24))
(declare-fun H_0_17 () (_ FloatingPoint 8 24))
(declare-fun H_0_18 () (_ FloatingPoint 8 24))
(declare-fun H_0_19 () (_ FloatingPoint 8 24))
(declare-fun H_0_20 () (_ FloatingPoint 8 24))
(declare-fun H_0_21 () (_ FloatingPoint 8 24))
(declare-fun H_0_22 () (_ FloatingPoint 8 24))
(declare-fun H_0_23 () (_ FloatingPoint 8 24))
(declare-fun H_0_24 () (_ FloatingPoint 8 24))
(declare-fun H_0_25 () (_ FloatingPoint 8 24))
(declare-fun H_0_26 () (_ FloatingPoint 8 24))
(declare-fun H_0_27 () (_ FloatingPoint 8 24))
(declare-fun H_0_28 () (_ FloatingPoint 8 24))
(declare-fun H_0_29 () (_ FloatingPoint 8 24))
(declare-fun H_0_30 () (_ FloatingPoint 8 24))
(declare-fun H_0_31 () (_ FloatingPoint 8 24))
(declare-fun H_0_32 () (_ FloatingPoint 8 24))
(declare-fun H_0_33 () (_ FloatingPoint 8 24))
(declare-fun H_0_34 () (_ FloatingPoint 8 24))
(declare-fun H_0_35 () (_ FloatingPoint 8 24))
(declare-fun H_0_36 () (_ FloatingPoint 8 24))
(declare-fun H_0_37 () (_ FloatingPoint 8 24))
(declare-fun H_0_38 () (_ FloatingPoint 8 24))
(declare-fun H_0_39 () (_ FloatingPoint 8 24))
(declare-fun H_0_40 () (_ FloatingPoint 8 24))
(declare-fun H_0_41 () (_ FloatingPoint 8 24))
(declare-fun H_0_42 () (_ FloatingPoint 8 24))
(declare-fun H_0_43 () (_ FloatingPoint 8 24))
(declare-fun H_0_44 () (_ FloatingPoint 8 24))
(declare-fun H_0_45 () (_ FloatingPoint 8 24))
(declare-fun H_0_46 () (_ FloatingPoint 8 24))
(assert (= H_0_0 (let ((a!1 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   (_ +zero 8 24)
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b0 #x7f #b00000000000000000000000)
                                           X_0))
                           (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_1))
                   (fp.mul roundNearestTiesToEven
                           (fp #b1 #x7f #b00000000000000000000000)
                           X_2))))
(let ((a!2 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   a!1
                                   (fp.mul roundNearestTiesToEven
                                           (_ +zero 8 24)
                                           X_3))
                           (fp.mul roundNearestTiesToEven
                                   (fp #b1 #x7f #b00000000000000000000000)
                                   X_4))
                   (fp.mul roundNearestTiesToEven
                           (fp #b1 #x7f #b00000000000000000000000)
                           X_5))))
  (fp.add roundNearestTiesToEven
          a!2
          (fp.mul roundNearestTiesToEven
                  (fp #b1 #x7f #b00000000000000000000000)
                  X_6))))))
(assert (= H_0_1 (let ((a!1 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   (_ +zero 8 24)
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b1 #x7f #b00000000000000000000000)
                                           X_0))
                           (fp.mul roundNearestTiesToEven
                                   (fp #b1 #x7f #b00000000000000000000000)
                                   X_1))
                   (fp.mul roundNearestTiesToEven
                           (fp #b1 #x7f #b00000000000000000000000)
                           X_2))))
(let ((a!2 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   a!1
                                   (fp.mul roundNearestTiesToEven
                                           (_ +zero 8 24)
                                           X_3))
                           (fp.mul roundNearestTiesToEven
                                   (fp #b1 #x7f #b00000000000000000000000)
                                   X_4))
                   (fp.mul roundNearestTiesToEven
                           (fp #b0 #x7f #b00000000000000000000000)
                           X_5))))
  (fp.add roundNearestTiesToEven
          a!2
          (fp.mul roundNearestTiesToEven
                  (fp #b1 #x7f #b00000000000000000000000)
                  X_6))))))
(assert (= H_0_2 (let ((a!1 (fp.add roundNearestTiesToEven
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
(let ((a!2 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   a!1
                                   (fp.mul roundNearestTiesToEven
                                           (_ +zero 8 24)
                                           X_3))
                           (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_4))
                   (fp.mul roundNearestTiesToEven
                           (fp #b1 #x7f #b00000000000000000000000)
                           X_5))))
  (fp.add roundNearestTiesToEven
          a!2
          (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_6))))))
(assert (= H_0_3 (let ((a!1 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   (fp #b1 #x80 #b00000000000000000000000)
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b0 #x7f #b00000000000000000000000)
                                           X_0))
                           (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_1))
                   (fp.mul roundNearestTiesToEven
                           (fp #b1 #x7f #b00000000000000000000000)
                           X_2))))
(let ((a!2 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   a!1
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b0 #x7f #b00000000000000000000000)
                                           X_3))
                           (fp.mul roundNearestTiesToEven
                                   (fp #b0 #x7f #b00000000000000000000000)
                                   X_4))
                   (fp.mul roundNearestTiesToEven
                           (fp #b1 #x7f #b00000000000000000000000)
                           X_5))))
  (fp.add roundNearestTiesToEven
          a!2
          (fp.mul roundNearestTiesToEven
                  (fp #b1 #x7f #b00000000000000000000000)
                  X_6))))))
(assert (= H_0_4 (let ((a!1 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   (fp #b1 #x81 #b00000000000000000000000)
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b0 #x7f #b00000000000000000000000)
                                           X_0))
                           (fp.mul roundNearestTiesToEven
                                   (fp #b0 #x7f #b00000000000000000000000)
                                   X_1))
                   (fp.mul roundNearestTiesToEven
                           (fp #b1 #x7f #b00000000000000000000000)
                           X_2))))
(let ((a!2 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   a!1
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b0 #x7f #b00000000000000000000000)
                                           X_3))
                           (fp.mul roundNearestTiesToEven
                                   (fp #b0 #x7f #b00000000000000000000000)
                                   X_4))
                   (fp.mul roundNearestTiesToEven
                           (fp #b0 #x7f #b00000000000000000000000)
                           X_5))))
  (fp.add roundNearestTiesToEven
          a!2
          (fp.mul roundNearestTiesToEven
                  (fp #b1 #x7f #b00000000000000000000000)
                  X_6))))))
(assert (= H_0_5 (let ((a!1 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   (fp #b1 #x80 #b00000000000000000000000)
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b0 #x7f #b00000000000000000000000)
                                           X_0))
                           (fp.mul roundNearestTiesToEven
                                   (fp #b1 #x7f #b00000000000000000000000)
                                   X_1))
                   (fp.mul roundNearestTiesToEven
                           (fp #b1 #x7f #b00000000000000000000000)
                           X_2))))
(let ((a!2 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   a!1
                                   (fp.mul roundNearestTiesToEven
                                           (_ +zero 8 24)
                                           X_3))
                           (fp.mul roundNearestTiesToEven
                                   (fp #b0 #x7f #b00000000000000000000000)
                                   X_4))
                   (fp.mul roundNearestTiesToEven
                           (fp #b0 #x7f #b00000000000000000000000)
                           X_5))))
  (fp.add roundNearestTiesToEven
          a!2
          (fp.mul roundNearestTiesToEven
                  (fp #b1 #x7f #b00000000000000000000000)
                  X_6))))))
(assert (= H_0_6 (let ((a!1 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   (fp #b1 #x7f #b00000000000000000000000)
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b0 #x7f #b00000000000000000000000)
                                           X_0))
                           (fp.mul roundNearestTiesToEven
                                   (fp #b1 #x7f #b00000000000000000000000)
                                   X_1))
                   (fp.mul roundNearestTiesToEven
                           (fp #b0 #x7f #b00000000000000000000000)
                           X_2))))
(let ((a!2 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   a!1
                                   (fp.mul roundNearestTiesToEven
                                           (_ +zero 8 24)
                                           X_3))
                           (fp.mul roundNearestTiesToEven
                                   (fp #b1 #x7f #b00000000000000000000000)
                                   X_4))
                   (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_5))))
  (fp.add roundNearestTiesToEven
          a!2
          (fp.mul roundNearestTiesToEven
                  (fp #b1 #x7f #b00000000000000000000000)
                  X_6))))))
(assert (= H_0_7 (let ((a!1 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   (fp #b1 #x7f #b00000000000000000000000)
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b1 #x7f #b00000000000000000000000)
                                           X_0))
                           (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_1))
                   (fp.mul roundNearestTiesToEven
                           (fp #b0 #x7f #b00000000000000000000000)
                           X_2))))
(let ((a!2 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   a!1
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b0 #x7f #b00000000000000000000000)
                                           X_3))
                           (fp.mul roundNearestTiesToEven
                                   (fp #b1 #x7f #b00000000000000000000000)
                                   X_4))
                   (fp.mul roundNearestTiesToEven
                           (fp #b1 #x7f #b00000000000000000000000)
                           X_5))))
  (fp.add roundNearestTiesToEven
          a!2
          (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_6))))))
(assert (= H_0_8 (let ((a!1 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   (fp #b1 #x80 #b10000000000000000000000)
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b0 #x7f #b00000000000000000000000)
                                           X_0))
                           (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_1))
                   (fp.mul roundNearestTiesToEven
                           (fp #b0 #x7f #b00000000000000000000000)
                           X_2))))
(let ((a!2 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   a!1
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b1 #x7f #b00000000000000000000000)
                                           X_3))
                           (fp.mul roundNearestTiesToEven
                                   (fp #b0 #x7f #b00000000000000000000000)
                                   X_4))
                   (fp.mul roundNearestTiesToEven
                           (fp #b0 #x7f #b00000000000000000000000)
                           X_5))))
  (fp.add roundNearestTiesToEven
          a!2
          (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_6))))))
(assert (= H_0_9 (let ((a!1 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   (fp #b1 #x80 #b00000000000000000000000)
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b1 #x7f #b00000000000000000000000)
                                           X_0))
                           (fp.mul roundNearestTiesToEven
                                   (fp #b1 #x7f #b00000000000000000000000)
                                   X_1))
                   (fp.mul roundNearestTiesToEven
                           (fp #b0 #x7f #b00000000000000000000000)
                           X_2))))
(let ((a!2 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   a!1
                                   (fp.mul roundNearestTiesToEven
                                           (_ +zero 8 24)
                                           X_3))
                           (fp.mul roundNearestTiesToEven
                                   (fp #b0 #x7f #b00000000000000000000000)
                                   X_4))
                   (fp.mul roundNearestTiesToEven
                           (fp #b0 #x7f #b00000000000000000000000)
                           X_5))))
  (fp.add roundNearestTiesToEven
          a!2
          (fp.mul roundNearestTiesToEven
                  (fp #b1 #x7f #b00000000000000000000000)
                  X_6))))))
(assert (= H_0_10 (let ((a!1 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   (fp #b1 #x80 #b10000000000000000000000)
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b0 #x7f #b00000000000000000000000)
                                           X_0))
                           (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_1))
                   (fp.mul roundNearestTiesToEven
                           (fp #b0 #x7f #b00000000000000000000000)
                           X_2))))
(let ((a!2 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   a!1
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b0 #x7f #b00000000000000000000000)
                                           X_3))
                           (fp.mul roundNearestTiesToEven
                                   (fp #b1 #x7f #b00000000000000000000000)
                                   X_4))
                   (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_5))))
  (fp.add roundNearestTiesToEven
          a!2
          (fp.mul roundNearestTiesToEven
                  (fp #b0 #x7f #b00000000000000000000000)
                  X_6))))))
(assert (= H_0_11 (let ((a!1 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   (fp #b1 #x7f #b00000000000000000000000)
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b0 #x7f #b00000000000000000000000)
                                           X_0))
                           (fp.mul roundNearestTiesToEven
                                   (fp #b1 #x7f #b00000000000000000000000)
                                   X_1))
                   (fp.mul roundNearestTiesToEven
                           (fp #b1 #x7f #b00000000000000000000000)
                           X_2))))
(let ((a!2 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   a!1
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b1 #x7f #b00000000000000000000000)
                                           X_3))
                           (fp.mul roundNearestTiesToEven
                                   (fp #b0 #x7f #b00000000000000000000000)
                                   X_4))
                   (fp.mul roundNearestTiesToEven
                           (fp #b1 #x7f #b00000000000000000000000)
                           X_5))))
  (fp.add roundNearestTiesToEven
          a!2
          (fp.mul roundNearestTiesToEven
                  (fp #b1 #x7f #b00000000000000000000000)
                  X_6))))))
(assert (= H_0_12 (let ((a!1 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   (fp #b1 #x80 #b00000000000000000000000)
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b0 #x7f #b00000000000000000000000)
                                           X_0))
                           (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_1))
                   (fp.mul roundNearestTiesToEven
                           (fp #b1 #x7f #b00000000000000000000000)
                           X_2))))
(let ((a!2 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   a!1
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b0 #x7f #b00000000000000000000000)
                                           X_3))
                           (fp.mul roundNearestTiesToEven
                                   (fp #b1 #x7f #b00000000000000000000000)
                                   X_4))
                   (fp.mul roundNearestTiesToEven
                           (fp #b0 #x7f #b00000000000000000000000)
                           X_5))))
  (fp.add roundNearestTiesToEven
          a!2
          (fp.mul roundNearestTiesToEven
                  (fp #b1 #x7f #b00000000000000000000000)
                  X_6))))))
(assert (= H_0_13 (let ((a!1 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   (fp #b1 #x80 #b10000000000000000000000)
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b0 #x7f #b00000000000000000000000)
                                           X_0))
                           (fp.mul roundNearestTiesToEven
                                   (fp #b0 #x7f #b00000000000000000000000)
                                   X_1))
                   (fp.mul roundNearestTiesToEven
                           (fp #b1 #x7f #b00000000000000000000000)
                           X_2))))
(let ((a!2 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   a!1
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b1 #x7f #b00000000000000000000000)
                                           X_3))
                           (fp.mul roundNearestTiesToEven
                                   (fp #b0 #x7f #b00000000000000000000000)
                                   X_4))
                   (fp.mul roundNearestTiesToEven
                           (fp #b0 #x7f #b00000000000000000000000)
                           X_5))))
  (fp.add roundNearestTiesToEven
          a!2
          (fp.mul roundNearestTiesToEven
                  (fp #b1 #x7f #b00000000000000000000000)
                  X_6))))))
(assert (= H_0_14 (let ((a!1 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   (fp #b1 #x7f #b00000000000000000000000)
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b1 #x7f #b00000000000000000000000)
                                           X_0))
                           (fp.mul roundNearestTiesToEven
                                   (fp #b1 #x7f #b00000000000000000000000)
                                   X_1))
                   (fp.mul roundNearestTiesToEven
                           (fp #b1 #x7f #b00000000000000000000000)
                           X_2))))
(let ((a!2 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   a!1
                                   (fp.mul roundNearestTiesToEven
                                           (_ +zero 8 24)
                                           X_3))
                           (fp.mul roundNearestTiesToEven
                                   (fp #b0 #x7f #b00000000000000000000000)
                                   X_4))
                   (fp.mul roundNearestTiesToEven
                           (fp #b0 #x7f #b00000000000000000000000)
                           X_5))))
  (fp.add roundNearestTiesToEven
          a!2
          (fp.mul roundNearestTiesToEven
                  (fp #b1 #x7f #b00000000000000000000000)
                  X_6))))))
(assert (= H_0_15 (let ((a!1 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   (fp #b1 #x80 #b00000000000000000000000)
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b0 #x7f #b00000000000000000000000)
                                           X_0))
                           (fp.mul roundNearestTiesToEven
                                   (fp #b0 #x7f #b00000000000000000000000)
                                   X_1))
                   (fp.mul roundNearestTiesToEven
                           (fp #b0 #x7f #b00000000000000000000000)
                           X_2))))
(let ((a!2 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   a!1
                                   (fp.mul roundNearestTiesToEven
                                           (_ +zero 8 24)
                                           X_3))
                           (fp.mul roundNearestTiesToEven
                                   (fp #b1 #x7f #b00000000000000000000000)
                                   X_4))
                   (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_5))))
  (fp.add roundNearestTiesToEven
          a!2
          (fp.mul roundNearestTiesToEven
                  (fp #b1 #x7f #b00000000000000000000000)
                  X_6))))))
(assert (= H_0_16 (let ((a!1 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   (fp #b1 #x80 #b00000000000000000000000)
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b1 #x7f #b00000000000000000000000)
                                           X_0))
                           (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_1))
                   (fp.mul roundNearestTiesToEven
                           (fp #b0 #x7f #b00000000000000000000000)
                           X_2))))
(let ((a!2 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   a!1
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b0 #x7f #b00000000000000000000000)
                                           X_3))
                           (fp.mul roundNearestTiesToEven
                                   (fp #b0 #x7f #b00000000000000000000000)
                                   X_4))
                   (fp.mul roundNearestTiesToEven
                           (fp #b1 #x7f #b00000000000000000000000)
                           X_5))))
  (fp.add roundNearestTiesToEven
          a!2
          (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_6))))))
(assert (= H_0_17 (let ((a!1 (fp.add roundNearestTiesToEven
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
(let ((a!2 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   a!1
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b1 #x7f #b00000000000000000000000)
                                           X_3))
                           (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_4))
                   (fp.mul roundNearestTiesToEven
                           (fp #b0 #x7f #b00000000000000000000000)
                           X_5))))
  (fp.add roundNearestTiesToEven
          a!2
          (fp.mul roundNearestTiesToEven
                  (fp #b1 #x7f #b00000000000000000000000)
                  X_6))))))
(assert (= H_0_18 (let ((a!1 (fp.add roundNearestTiesToEven
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
(let ((a!2 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   a!1
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b1 #x7f #b00000000000000000000000)
                                           X_3))
                           (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_4))
                   (fp.mul roundNearestTiesToEven
                           (fp #b0 #x7f #b00000000000000000000000)
                           X_5))))
  (fp.add roundNearestTiesToEven
          a!2
          (fp.mul roundNearestTiesToEven
                  (fp #b1 #x7f #b00000000000000000000000)
                  X_6))))))
(assert (= H_0_19 (let ((a!1 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   (fp #b1 #x80 #b00000000000000000000000)
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b1 #x7f #b00000000000000000000000)
                                           X_0))
                           (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_1))
                   (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_2))))
(let ((a!2 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   a!1
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b0 #x7f #b00000000000000000000000)
                                           X_3))
                           (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_4))
                   (fp.mul roundNearestTiesToEven
                           (fp #b0 #x7f #b00000000000000000000000)
                           X_5))))
  (fp.add roundNearestTiesToEven
          a!2
          (fp.mul roundNearestTiesToEven
                  (fp #b0 #x7f #b00000000000000000000000)
                  X_6))))))
(assert (= H_0_20 (let ((a!1 (fp.add roundNearestTiesToEven
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
(let ((a!2 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   a!1
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b1 #x7f #b00000000000000000000000)
                                           X_3))
                           (fp.mul roundNearestTiesToEven
                                   (fp #b1 #x7f #b00000000000000000000000)
                                   X_4))
                   (fp.mul roundNearestTiesToEven
                           (fp #b1 #x7f #b00000000000000000000000)
                           X_5))))
  (fp.add roundNearestTiesToEven
          a!2
          (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_6))))))
(assert (= H_0_21 (let ((a!1 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   (fp #b1 #x81 #b00000000000000000000000)
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b0 #x7f #b00000000000000000000000)
                                           X_0))
                           (fp.mul roundNearestTiesToEven
                                   (fp #b1 #x7f #b00000000000000000000000)
                                   X_1))
                   (fp.mul roundNearestTiesToEven
                           (fp #b0 #x7f #b00000000000000000000000)
                           X_2))))
(let ((a!2 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   a!1
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b0 #x7f #b00000000000000000000000)
                                           X_3))
                           (fp.mul roundNearestTiesToEven
                                   (fp #b0 #x7f #b00000000000000000000000)
                                   X_4))
                   (fp.mul roundNearestTiesToEven
                           (fp #b0 #x7f #b00000000000000000000000)
                           X_5))))
  (fp.add roundNearestTiesToEven
          a!2
          (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_6))))))
(assert (= H_0_22 (let ((a!1 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   (fp #b1 #x80 #b00000000000000000000000)
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b1 #x7f #b00000000000000000000000)
                                           X_0))
                           (fp.mul roundNearestTiesToEven
                                   (fp #b0 #x7f #b00000000000000000000000)
                                   X_1))
                   (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_2))))
(let ((a!2 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   a!1
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b0 #x7f #b00000000000000000000000)
                                           X_3))
                           (fp.mul roundNearestTiesToEven
                                   (fp #b1 #x7f #b00000000000000000000000)
                                   X_4))
                   (fp.mul roundNearestTiesToEven
                           (fp #b0 #x7f #b00000000000000000000000)
                           X_5))))
  (fp.add roundNearestTiesToEven
          a!2
          (fp.mul roundNearestTiesToEven
                  (fp #b1 #x7f #b00000000000000000000000)
                  X_6))))))
(assert (= H_0_23 (let ((a!1 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   (fp #b1 #x80 #b00000000000000000000000)
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b0 #x7f #b00000000000000000000000)
                                           X_0))
                           (fp.mul roundNearestTiesToEven
                                   (fp #b0 #x7f #b00000000000000000000000)
                                   X_1))
                   (fp.mul roundNearestTiesToEven
                           (fp #b1 #x7f #b00000000000000000000000)
                           X_2))))
(let ((a!2 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   a!1
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b1 #x7f #b00000000000000000000000)
                                           X_3))
                           (fp.mul roundNearestTiesToEven
                                   (fp #b0 #x7f #b00000000000000000000000)
                                   X_4))
                   (fp.mul roundNearestTiesToEven
                           (fp #b1 #x7f #b00000000000000000000000)
                           X_5))))
  (fp.add roundNearestTiesToEven
          a!2
          (fp.mul roundNearestTiesToEven
                  (fp #b1 #x7f #b00000000000000000000000)
                  X_6))))))
(assert (= H_0_24 (let ((a!1 (fp.add roundNearestTiesToEven
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
(let ((a!2 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   a!1
                                   (fp.mul roundNearestTiesToEven
                                           (_ +zero 8 24)
                                           X_3))
                           (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_4))
                   (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_5))))
  (fp.add roundNearestTiesToEven
          a!2
          (fp.mul roundNearestTiesToEven
                  (fp #b0 #x7f #b00000000000000000000000)
                  X_6))))))
(assert (= H_0_25 (let ((a!1 (fp.add roundNearestTiesToEven
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
(let ((a!2 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   a!1
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b1 #x7f #b00000000000000000000000)
                                           X_3))
                           (fp.mul roundNearestTiesToEven
                                   (fp #b1 #x7f #b00000000000000000000000)
                                   X_4))
                   (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_5))))
  (fp.add roundNearestTiesToEven
          a!2
          (fp.mul roundNearestTiesToEven
                  (fp #b0 #x7f #b00000000000000000000000)
                  X_6))))))
(assert (= H_0_26 (let ((a!1 (fp.add roundNearestTiesToEven
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
(let ((a!2 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   a!1
                                   (fp.mul roundNearestTiesToEven
                                           (_ +zero 8 24)
                                           X_3))
                           (fp.mul roundNearestTiesToEven
                                   (fp #b0 #x7f #b00000000000000000000000)
                                   X_4))
                   (fp.mul roundNearestTiesToEven
                           (fp #b1 #x7f #b00000000000000000000000)
                           X_5))))
  (fp.add roundNearestTiesToEven
          a!2
          (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_6))))))
(assert (= H_0_27 (let ((a!1 (fp.add roundNearestTiesToEven
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
(let ((a!2 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   a!1
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b1 #x7f #b00000000000000000000000)
                                           X_3))
                           (fp.mul roundNearestTiesToEven
                                   (fp #b1 #x7f #b00000000000000000000000)
                                   X_4))
                   (fp.mul roundNearestTiesToEven
                           (fp #b0 #x7f #b00000000000000000000000)
                           X_5))))
  (fp.add roundNearestTiesToEven
          a!2
          (fp.mul roundNearestTiesToEven
                  (fp #b1 #x7f #b00000000000000000000000)
                  X_6))))))
(assert (= H_0_28 (let ((a!1 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   (fp #b1 #x7f #b00000000000000000000000)
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b1 #x7f #b00000000000000000000000)
                                           X_0))
                           (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_1))
                   (fp.mul roundNearestTiesToEven
                           (fp #b0 #x7f #b00000000000000000000000)
                           X_2))))
(let ((a!2 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   a!1
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b1 #x7f #b00000000000000000000000)
                                           X_3))
                           (fp.mul roundNearestTiesToEven
                                   (fp #b0 #x7f #b00000000000000000000000)
                                   X_4))
                   (fp.mul roundNearestTiesToEven
                           (fp #b1 #x7f #b00000000000000000000000)
                           X_5))))
  (fp.add roundNearestTiesToEven
          a!2
          (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_6))))))
(assert (= H_0_29 (let ((a!1 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   (fp #b1 #x80 #b10000000000000000000000)
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b1 #x7f #b00000000000000000000000)
                                           X_0))
                           (fp.mul roundNearestTiesToEven
                                   (fp #b0 #x7f #b00000000000000000000000)
                                   X_1))
                   (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_2))))
(let ((a!2 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   a!1
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b0 #x7f #b00000000000000000000000)
                                           X_3))
                           (fp.mul roundNearestTiesToEven
                                   (fp #b0 #x7f #b00000000000000000000000)
                                   X_4))
                   (fp.mul roundNearestTiesToEven
                           (fp #b0 #x7f #b00000000000000000000000)
                           X_5))))
  (fp.add roundNearestTiesToEven
          a!2
          (fp.mul roundNearestTiesToEven
                  (fp #b1 #x7f #b00000000000000000000000)
                  X_6))))))
(assert (= H_0_30 (let ((a!1 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   (fp #b1 #x81 #b01000000000000000000000)
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b0 #x7f #b00000000000000000000000)
                                           X_0))
                           (fp.mul roundNearestTiesToEven
                                   (fp #b0 #x7f #b00000000000000000000000)
                                   X_1))
                   (fp.mul roundNearestTiesToEven
                           (fp #b0 #x7f #b00000000000000000000000)
                           X_2))))
(let ((a!2 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   a!1
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b0 #x7f #b00000000000000000000000)
                                           X_3))
                           (fp.mul roundNearestTiesToEven
                                   (fp #b0 #x7f #b00000000000000000000000)
                                   X_4))
                   (fp.mul roundNearestTiesToEven
                           (fp #b0 #x7f #b00000000000000000000000)
                           X_5))))
  (fp.add roundNearestTiesToEven
          a!2
          (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_6))))))
(assert (= H_0_31 (let ((a!1 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   (fp #b1 #x7f #b00000000000000000000000)
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b1 #x7f #b00000000000000000000000)
                                           X_0))
                           (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_1))
                   (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_2))))
(let ((a!2 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   a!1
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b1 #x7f #b00000000000000000000000)
                                           X_3))
                           (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_4))
                   (fp.mul roundNearestTiesToEven
                           (fp #b0 #x7f #b00000000000000000000000)
                           X_5))))
  (fp.add roundNearestTiesToEven
          a!2
          (fp.mul roundNearestTiesToEven
                  (fp #b0 #x7f #b00000000000000000000000)
                  X_6))))))
(assert (= H_0_32 (let ((a!1 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   (fp #b1 #x7f #b00000000000000000000000)
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b1 #x7f #b00000000000000000000000)
                                           X_0))
                           (fp.mul roundNearestTiesToEven
                                   (fp #b1 #x7f #b00000000000000000000000)
                                   X_1))
                   (fp.mul roundNearestTiesToEven
                           (fp #b0 #x7f #b00000000000000000000000)
                           X_2))))
(let ((a!2 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   a!1
                                   (fp.mul roundNearestTiesToEven
                                           (_ +zero 8 24)
                                           X_3))
                           (fp.mul roundNearestTiesToEven
                                   (fp #b1 #x7f #b00000000000000000000000)
                                   X_4))
                   (fp.mul roundNearestTiesToEven
                           (fp #b0 #x7f #b00000000000000000000000)
                           X_5))))
  (fp.add roundNearestTiesToEven
          a!2
          (fp.mul roundNearestTiesToEven
                  (fp #b1 #x7f #b00000000000000000000000)
                  X_6))))))
(assert (= H_0_33 (let ((a!1 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   (_ +zero 8 24)
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b0 #x7f #b00000000000000000000000)
                                           X_0))
                           (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_1))
                   (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_2))))
(let ((a!2 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   a!1
                                   (fp.mul roundNearestTiesToEven
                                           (_ +zero 8 24)
                                           X_3))
                           (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_4))
                   (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_5))))
  (fp.add roundNearestTiesToEven
          a!2
          (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_6))))))
(assert (= H_0_34 (let ((a!1 (fp.add roundNearestTiesToEven
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
(let ((a!2 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   a!1
                                   (fp.mul roundNearestTiesToEven
                                           (_ +zero 8 24)
                                           X_3))
                           (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_4))
                   (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_5))))
  (fp.add roundNearestTiesToEven
          a!2
          (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_6))))))
(assert (= H_0_35 (let ((a!1 (fp.add roundNearestTiesToEven
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
(let ((a!2 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   a!1
                                   (fp.mul roundNearestTiesToEven
                                           (_ +zero 8 24)
                                           X_3))
                           (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_4))
                   (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_5))))
  (fp.add roundNearestTiesToEven
          a!2
          (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_6))))))
(assert (= H_0_36 (let ((a!1 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   (_ +zero 8 24)
                                   (fp.mul roundNearestTiesToEven
                                           (_ +zero 8 24)
                                           X_0))
                           (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_1))
                   (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_2))))
(let ((a!2 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   a!1
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b0 #x7f #b00000000000000000000000)
                                           X_3))
                           (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_4))
                   (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_5))))
  (fp.add roundNearestTiesToEven
          a!2
          (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_6))))))
(assert (= H_0_37 (let ((a!1 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   (_ +zero 8 24)
                                   (fp.mul roundNearestTiesToEven
                                           (_ +zero 8 24)
                                           X_0))
                           (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_1))
                   (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_2))))
(let ((a!2 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   a!1
                                   (fp.mul roundNearestTiesToEven
                                           (_ +zero 8 24)
                                           X_3))
                           (fp.mul roundNearestTiesToEven
                                   (fp #b0 #x7f #b00000000000000000000000)
                                   X_4))
                   (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_5))))
  (fp.add roundNearestTiesToEven
          a!2
          (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_6))))))
(assert (= H_0_38 (let ((a!1 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   (_ +zero 8 24)
                                   (fp.mul roundNearestTiesToEven
                                           (_ +zero 8 24)
                                           X_0))
                           (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_1))
                   (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_2))))
(let ((a!2 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   a!1
                                   (fp.mul roundNearestTiesToEven
                                           (_ +zero 8 24)
                                           X_3))
                           (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_4))
                   (fp.mul roundNearestTiesToEven
                           (fp #b0 #x7f #b00000000000000000000000)
                           X_5))))
  (fp.add roundNearestTiesToEven
          a!2
          (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_6))))))
(assert (= H_0_39 (let ((a!1 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   (_ +zero 8 24)
                                   (fp.mul roundNearestTiesToEven
                                           (_ +zero 8 24)
                                           X_0))
                           (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_1))
                   (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_2))))
(let ((a!2 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   a!1
                                   (fp.mul roundNearestTiesToEven
                                           (_ +zero 8 24)
                                           X_3))
                           (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_4))
                   (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_5))))
  (fp.add roundNearestTiesToEven
          a!2
          (fp.mul roundNearestTiesToEven
                  (fp #b0 #x7f #b00000000000000000000000)
                  X_6))))))
(assert (= H_0_40 (let ((a!1 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   (fp #b1 #x7f #b00000000000000000000000)
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b0 #x80 #b00000000000000000000000)
                                           X_0))
                           (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_1))
                   (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_2))))
(let ((a!2 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   a!1
                                   (fp.mul roundNearestTiesToEven
                                           (_ +zero 8 24)
                                           X_3))
                           (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_4))
                   (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_5))))
  (fp.add roundNearestTiesToEven
          a!2
          (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_6))))))
(assert (= H_0_41 (let ((a!1 (fp.add roundNearestTiesToEven
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
(let ((a!2 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   a!1
                                   (fp.mul roundNearestTiesToEven
                                           (_ +zero 8 24)
                                           X_3))
                           (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_4))
                   (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_5))))
  (fp.add roundNearestTiesToEven
          a!2
          (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_6))))))
(assert (= H_0_42 (let ((a!1 (fp.add roundNearestTiesToEven
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
(let ((a!2 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   a!1
                                   (fp.mul roundNearestTiesToEven
                                           (_ +zero 8 24)
                                           X_3))
                           (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_4))
                   (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_5))))
  (fp.add roundNearestTiesToEven
          a!2
          (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_6))))))
(assert (= H_0_43 (let ((a!1 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   (fp #b1 #x7f #b00000000000000000000000)
                                   (fp.mul roundNearestTiesToEven
                                           (_ +zero 8 24)
                                           X_0))
                           (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_1))
                   (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_2))))
(let ((a!2 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   a!1
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b0 #x80 #b00000000000000000000000)
                                           X_3))
                           (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_4))
                   (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_5))))
  (fp.add roundNearestTiesToEven
          a!2
          (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_6))))))
(assert (= H_0_44 (let ((a!1 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   (fp #b1 #x7f #b00000000000000000000000)
                                   (fp.mul roundNearestTiesToEven
                                           (_ +zero 8 24)
                                           X_0))
                           (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_1))
                   (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_2))))
(let ((a!2 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   a!1
                                   (fp.mul roundNearestTiesToEven
                                           (_ +zero 8 24)
                                           X_3))
                           (fp.mul roundNearestTiesToEven
                                   (fp #b0 #x80 #b00000000000000000000000)
                                   X_4))
                   (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_5))))
  (fp.add roundNearestTiesToEven
          a!2
          (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_6))))))
(assert (= H_0_45 (let ((a!1 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   (fp #b1 #x7f #b00000000000000000000000)
                                   (fp.mul roundNearestTiesToEven
                                           (_ +zero 8 24)
                                           X_0))
                           (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_1))
                   (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_2))))
(let ((a!2 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   a!1
                                   (fp.mul roundNearestTiesToEven
                                           (_ +zero 8 24)
                                           X_3))
                           (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_4))
                   (fp.mul roundNearestTiesToEven
                           (fp #b0 #x80 #b00000000000000000000000)
                           X_5))))
  (fp.add roundNearestTiesToEven
          a!2
          (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_6))))))
(assert (= H_0_46 (let ((a!1 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   (fp #b1 #x7f #b00000000000000000000000)
                                   (fp.mul roundNearestTiesToEven
                                           (_ +zero 8 24)
                                           X_0))
                           (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_1))
                   (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_2))))
(let ((a!2 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   a!1
                                   (fp.mul roundNearestTiesToEven
                                           (_ +zero 8 24)
                                           X_3))
                           (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_4))
                   (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_5))))
  (fp.add roundNearestTiesToEven
          a!2
          (fp.mul roundNearestTiesToEven
                  (fp #b0 #x80 #b00000000000000000000000)
                  X_6))))))
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
(declare-fun H_1_16 () (_ FloatingPoint 8 24))
(declare-fun H_1_17 () (_ FloatingPoint 8 24))
(declare-fun H_1_18 () (_ FloatingPoint 8 24))
(declare-fun H_1_19 () (_ FloatingPoint 8 24))
(declare-fun H_1_20 () (_ FloatingPoint 8 24))
(declare-fun H_1_21 () (_ FloatingPoint 8 24))
(declare-fun H_1_22 () (_ FloatingPoint 8 24))
(declare-fun H_1_23 () (_ FloatingPoint 8 24))
(declare-fun H_1_24 () (_ FloatingPoint 8 24))
(declare-fun H_1_25 () (_ FloatingPoint 8 24))
(declare-fun H_1_26 () (_ FloatingPoint 8 24))
(declare-fun H_1_27 () (_ FloatingPoint 8 24))
(declare-fun H_1_28 () (_ FloatingPoint 8 24))
(declare-fun H_1_29 () (_ FloatingPoint 8 24))
(declare-fun H_1_30 () (_ FloatingPoint 8 24))
(declare-fun H_1_31 () (_ FloatingPoint 8 24))
(declare-fun H_1_32 () (_ FloatingPoint 8 24))
(declare-fun H_1_33 () (_ FloatingPoint 8 24))
(declare-fun H_1_34 () (_ FloatingPoint 8 24))
(declare-fun H_1_35 () (_ FloatingPoint 8 24))
(declare-fun H_1_36 () (_ FloatingPoint 8 24))
(declare-fun H_1_37 () (_ FloatingPoint 8 24))
(declare-fun H_1_38 () (_ FloatingPoint 8 24))
(declare-fun H_1_39 () (_ FloatingPoint 8 24))
(declare-fun H_1_40 () (_ FloatingPoint 8 24))
(declare-fun H_1_41 () (_ FloatingPoint 8 24))
(declare-fun H_1_42 () (_ FloatingPoint 8 24))
(declare-fun H_1_43 () (_ FloatingPoint 8 24))
(declare-fun H_1_44 () (_ FloatingPoint 8 24))
(declare-fun H_1_45 () (_ FloatingPoint 8 24))
(declare-fun H_1_46 () (_ FloatingPoint 8 24))
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
(assert (= H_1_16 (ite (fp.geq H_0_16 (_ +zero 8 24)) H_0_16 (_ +zero 8 24))))
(assert (= H_1_17 (ite (fp.geq H_0_17 (_ +zero 8 24)) H_0_17 (_ +zero 8 24))))
(assert (= H_1_18 (ite (fp.geq H_0_18 (_ +zero 8 24)) H_0_18 (_ +zero 8 24))))
(assert (= H_1_19 (ite (fp.geq H_0_19 (_ +zero 8 24)) H_0_19 (_ +zero 8 24))))
(assert (= H_1_20 (ite (fp.geq H_0_20 (_ +zero 8 24)) H_0_20 (_ +zero 8 24))))
(assert (= H_1_21 (ite (fp.geq H_0_21 (_ +zero 8 24)) H_0_21 (_ +zero 8 24))))
(assert (= H_1_22 (ite (fp.geq H_0_22 (_ +zero 8 24)) H_0_22 (_ +zero 8 24))))
(assert (= H_1_23 (ite (fp.geq H_0_23 (_ +zero 8 24)) H_0_23 (_ +zero 8 24))))
(assert (= H_1_24 (ite (fp.geq H_0_24 (_ +zero 8 24)) H_0_24 (_ +zero 8 24))))
(assert (= H_1_25 (ite (fp.geq H_0_25 (_ +zero 8 24)) H_0_25 (_ +zero 8 24))))
(assert (= H_1_26 (ite (fp.geq H_0_26 (_ +zero 8 24)) H_0_26 (_ +zero 8 24))))
(assert (= H_1_27 (ite (fp.geq H_0_27 (_ +zero 8 24)) H_0_27 (_ +zero 8 24))))
(assert (= H_1_28 (ite (fp.geq H_0_28 (_ +zero 8 24)) H_0_28 (_ +zero 8 24))))
(assert (= H_1_29 (ite (fp.geq H_0_29 (_ +zero 8 24)) H_0_29 (_ +zero 8 24))))
(assert (= H_1_30 (ite (fp.geq H_0_30 (_ +zero 8 24)) H_0_30 (_ +zero 8 24))))
(assert (= H_1_31 (ite (fp.geq H_0_31 (_ +zero 8 24)) H_0_31 (_ +zero 8 24))))
(assert (= H_1_32 (ite (fp.geq H_0_32 (_ +zero 8 24)) H_0_32 (_ +zero 8 24))))
(assert (= H_1_33 (ite (fp.geq H_0_33 (_ +zero 8 24)) H_0_33 (_ +zero 8 24))))
(assert (= H_1_34 (ite (fp.geq H_0_34 (_ +zero 8 24)) H_0_34 (_ +zero 8 24))))
(assert (= H_1_35 (ite (fp.geq H_0_35 (_ +zero 8 24)) H_0_35 (_ +zero 8 24))))
(assert (= H_1_36 (ite (fp.geq H_0_36 (_ +zero 8 24)) H_0_36 (_ +zero 8 24))))
(assert (= H_1_37 (ite (fp.geq H_0_37 (_ +zero 8 24)) H_0_37 (_ +zero 8 24))))
(assert (= H_1_38 (ite (fp.geq H_0_38 (_ +zero 8 24)) H_0_38 (_ +zero 8 24))))
(assert (= H_1_39 (ite (fp.geq H_0_39 (_ +zero 8 24)) H_0_39 (_ +zero 8 24))))
(assert (= H_1_40 (ite (fp.geq H_0_40 (_ +zero 8 24)) H_0_40 (_ +zero 8 24))))
(assert (= H_1_41 (ite (fp.geq H_0_41 (_ +zero 8 24)) H_0_41 (_ +zero 8 24))))
(assert (= H_1_42 (ite (fp.geq H_0_42 (_ +zero 8 24)) H_0_42 (_ +zero 8 24))))
(assert (= H_1_43 (ite (fp.geq H_0_43 (_ +zero 8 24)) H_0_43 (_ +zero 8 24))))
(assert (= H_1_44 (ite (fp.geq H_0_44 (_ +zero 8 24)) H_0_44 (_ +zero 8 24))))
(assert (= H_1_45 (ite (fp.geq H_0_45 (_ +zero 8 24)) H_0_45 (_ +zero 8 24))))
(assert (= H_1_46 (ite (fp.geq H_0_46 (_ +zero 8 24)) H_0_46 (_ +zero 8 24))))
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
                   (fp.mul roundNearestTiesToEven
                           (fp #b1 #x7f #b00000000000000000000000)
                           H_1_8))))
(let ((a!4 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   a!3
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b1 #x7f #b00000000000000000000000)
                                           H_1_9))
                           (fp.mul roundNearestTiesToEven
                                   (fp #b1 #x7f #b00000000000000000000000)
                                   H_1_10))
                   (fp.mul roundNearestTiesToEven
                           (fp #b1 #x7f #b00000000000000000000000)
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
(let ((a!6 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   a!5
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b1 #x7f #b00000000000000000000000)
                                           H_1_15))
                           (fp.mul roundNearestTiesToEven
                                   (fp #b1 #x7f #b00000000000000000000000)
                                   H_1_16))
                   (fp.mul roundNearestTiesToEven
                           (fp #b1 #x7f #b00000000000000000000000)
                           H_1_17))))
(let ((a!7 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   a!6
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b1 #x7f #b00000000000000000000000)
                                           H_1_18))
                           (fp.mul roundNearestTiesToEven
                                   (fp #b1 #x7f #b00000000000000000000000)
                                   H_1_19))
                   (fp.mul roundNearestTiesToEven
                           (fp #b1 #x7f #b00000000000000000000000)
                           H_1_20))))
(let ((a!8 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   a!7
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b1 #x7f #b00000000000000000000000)
                                           H_1_21))
                           (fp.mul roundNearestTiesToEven
                                   (fp #b1 #x7f #b00000000000000000000000)
                                   H_1_22))
                   (fp.mul roundNearestTiesToEven
                           (fp #b1 #x7f #b00000000000000000000000)
                           H_1_23))))
(let ((a!9 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   a!8
                                   (fp.mul roundNearestTiesToEven
                                           (fp #b1 #x7f #b00000000000000000000000)
                                           H_1_24))
                           (fp.mul roundNearestTiesToEven
                                   (fp #b1 #x7f #b00000000000000000000000)
                                   H_1_25))
                   (fp.mul roundNearestTiesToEven
                           (fp #b1 #x7f #b00000000000000000000000)
                           H_1_26))))
(let ((a!10 (fp.add roundNearestTiesToEven
                    (fp.add roundNearestTiesToEven
                            (fp.add roundNearestTiesToEven
                                    a!9
                                    (fp.mul roundNearestTiesToEven
                                            (fp #b1 #x7f #b00000000000000000000000)
                                            H_1_27))
                            (fp.mul roundNearestTiesToEven
                                    (fp #b1 #x7f #b00000000000000000000000)
                                    H_1_28))
                    (fp.mul roundNearestTiesToEven
                            (fp #b1 #x7f #b00000000000000000000000)
                            H_1_29))))
(let ((a!11 (fp.add roundNearestTiesToEven
                    (fp.add roundNearestTiesToEven
                            (fp.add roundNearestTiesToEven
                                    a!10
                                    (fp.mul roundNearestTiesToEven
                                            (fp #b1 #x7f #b00000000000000000000000)
                                            H_1_30))
                            (fp.mul roundNearestTiesToEven
                                    (fp #b1 #x7f #b00000000000000000000000)
                                    H_1_31))
                    (fp.mul roundNearestTiesToEven
                            (fp #b1 #x7f #b00000000000000000000000)
                            H_1_32))))
(let ((a!12 (fp.add roundNearestTiesToEven
                    (fp.add roundNearestTiesToEven
                            (fp.add roundNearestTiesToEven
                                    a!11
                                    (fp.mul roundNearestTiesToEven
                                            (_ +zero 8 24)
                                            H_1_33))
                            (fp.mul roundNearestTiesToEven
                                    (_ +zero 8 24)
                                    H_1_34))
                    (fp.mul roundNearestTiesToEven (_ +zero 8 24) H_1_35))))
(let ((a!13 (fp.add roundNearestTiesToEven
                    (fp.add roundNearestTiesToEven
                            (fp.add roundNearestTiesToEven
                                    a!12
                                    (fp.mul roundNearestTiesToEven
                                            (_ +zero 8 24)
                                            H_1_36))
                            (fp.mul roundNearestTiesToEven
                                    (_ +zero 8 24)
                                    H_1_37))
                    (fp.mul roundNearestTiesToEven (_ +zero 8 24) H_1_38))))
(let ((a!14 (fp.add roundNearestTiesToEven
                    (fp.add roundNearestTiesToEven
                            (fp.add roundNearestTiesToEven
                                    a!13
                                    (fp.mul roundNearestTiesToEven
                                            (_ +zero 8 24)
                                            H_1_39))
                            (fp.mul roundNearestTiesToEven
                                    (_ +zero 8 24)
                                    H_1_40))
                    (fp.mul roundNearestTiesToEven (_ +zero 8 24) H_1_41))))
(let ((a!15 (fp.add roundNearestTiesToEven
                    (fp.add roundNearestTiesToEven
                            (fp.add roundNearestTiesToEven
                                    a!14
                                    (fp.mul roundNearestTiesToEven
                                            (_ +zero 8 24)
                                            H_1_42))
                            (fp.mul roundNearestTiesToEven
                                    (_ +zero 8 24)
                                    H_1_43))
                    (fp.mul roundNearestTiesToEven (_ +zero 8 24) H_1_44))))
  (fp.add roundNearestTiesToEven
          (fp.add roundNearestTiesToEven
                  a!15
                  (fp.mul roundNearestTiesToEven (_ +zero 8 24) H_1_45))
          (fp.mul roundNearestTiesToEven (_ +zero 8 24) H_1_46)))))))))))))))))))
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
(let ((a!6 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   a!5
                                   (fp.mul roundNearestTiesToEven
                                           (_ +zero 8 24)
                                           H_1_15))
                           (fp.mul roundNearestTiesToEven (_ +zero 8 24) H_1_16))
                   (fp.mul roundNearestTiesToEven (_ +zero 8 24) H_1_17))))
(let ((a!7 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   a!6
                                   (fp.mul roundNearestTiesToEven
                                           (_ +zero 8 24)
                                           H_1_18))
                           (fp.mul roundNearestTiesToEven (_ +zero 8 24) H_1_19))
                   (fp.mul roundNearestTiesToEven (_ +zero 8 24) H_1_20))))
(let ((a!8 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   a!7
                                   (fp.mul roundNearestTiesToEven
                                           (_ +zero 8 24)
                                           H_1_21))
                           (fp.mul roundNearestTiesToEven (_ +zero 8 24) H_1_22))
                   (fp.mul roundNearestTiesToEven (_ +zero 8 24) H_1_23))))
(let ((a!9 (fp.add roundNearestTiesToEven
                   (fp.add roundNearestTiesToEven
                           (fp.add roundNearestTiesToEven
                                   a!8
                                   (fp.mul roundNearestTiesToEven
                                           (_ +zero 8 24)
                                           H_1_24))
                           (fp.mul roundNearestTiesToEven (_ +zero 8 24) H_1_25))
                   (fp.mul roundNearestTiesToEven (_ +zero 8 24) H_1_26))))
(let ((a!10 (fp.add roundNearestTiesToEven
                    (fp.add roundNearestTiesToEven
                            (fp.add roundNearestTiesToEven
                                    a!9
                                    (fp.mul roundNearestTiesToEven
                                            (_ +zero 8 24)
                                            H_1_27))
                            (fp.mul roundNearestTiesToEven
                                    (_ +zero 8 24)
                                    H_1_28))
                    (fp.mul roundNearestTiesToEven (_ +zero 8 24) H_1_29))))
(let ((a!11 (fp.add roundNearestTiesToEven
                    (fp.add roundNearestTiesToEven
                            (fp.add roundNearestTiesToEven
                                    a!10
                                    (fp.mul roundNearestTiesToEven
                                            (_ +zero 8 24)
                                            H_1_30))
                            (fp.mul roundNearestTiesToEven
                                    (_ +zero 8 24)
                                    H_1_31))
                    (fp.mul roundNearestTiesToEven (_ +zero 8 24) H_1_32))))
(let ((a!12 (fp.add roundNearestTiesToEven
                    (fp.add roundNearestTiesToEven
                            (fp.add roundNearestTiesToEven
                                    a!11
                                    (fp.mul roundNearestTiesToEven
                                            (fp #b0 #x7f #b00000000000000000000000)
                                            H_1_33))
                            (fp.mul roundNearestTiesToEven
                                    (fp #b0 #x7f #b00000000000000000000000)
                                    H_1_34))
                    (fp.mul roundNearestTiesToEven
                            (fp #b0 #x7f #b00000000000000000000000)
                            H_1_35))))
(let ((a!13 (fp.add roundNearestTiesToEven
                    (fp.add roundNearestTiesToEven
                            (fp.add roundNearestTiesToEven
                                    a!12
                                    (fp.mul roundNearestTiesToEven
                                            (fp #b0 #x7f #b00000000000000000000000)
                                            H_1_36))
                            (fp.mul roundNearestTiesToEven
                                    (fp #b0 #x7f #b00000000000000000000000)
                                    H_1_37))
                    (fp.mul roundNearestTiesToEven
                            (fp #b0 #x7f #b00000000000000000000000)
                            H_1_38))))
(let ((a!14 (fp.add roundNearestTiesToEven
                    (fp.add roundNearestTiesToEven
                            (fp.add roundNearestTiesToEven
                                    a!13
                                    (fp.mul roundNearestTiesToEven
                                            (fp #b0 #x7f #b00000000000000000000000)
                                            H_1_39))
                            (fp.mul roundNearestTiesToEven
                                    (fp #b1 #x7f #b00000000000000000000000)
                                    H_1_40))
                    (fp.mul roundNearestTiesToEven
                            (fp #b1 #x7f #b00000000000000000000000)
                            H_1_41))))
(let ((a!15 (fp.add roundNearestTiesToEven
                    (fp.add roundNearestTiesToEven
                            (fp.add roundNearestTiesToEven
                                    a!14
                                    (fp.mul roundNearestTiesToEven
                                            (fp #b1 #x7f #b00000000000000000000000)
                                            H_1_42))
                            (fp.mul roundNearestTiesToEven
                                    (fp #b1 #x7f #b00000000000000000000000)
                                    H_1_43))
                    (fp.mul roundNearestTiesToEven
                            (fp #b1 #x7f #b00000000000000000000000)
                            H_1_44))))
  (fp.add roundNearestTiesToEven
          (fp.add roundNearestTiesToEven
                  a!15
                  (fp.mul roundNearestTiesToEven
                          (fp #b1 #x7f #b00000000000000000000000)
                          H_1_45))
          (fp.mul roundNearestTiesToEven
                  (fp #b1 #x7f #b00000000000000000000000)
                  H_1_46)))))))))))))))))))
(declare-fun Y_0 () (_ FloatingPoint 8 24))
(assert (= Y_0 H_2_0))
(declare-fun Y_1 () (_ FloatingPoint 8 24))
(assert (= Y_1 H_2_1))
(assert (fp.geq Y_0 (fp #b0 #x7f #b00000000000000000000000)))
(assert (fp.leq Y_1 (_ +zero 8 24)))
(check-sat)
(get-model)