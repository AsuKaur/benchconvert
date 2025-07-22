(set-logic QF_BVFP)
(declare-fun X_0 () (_ FloatingPoint 8 24))
(declare-fun X_1 () (_ FloatingPoint 8 24))
(assert (fp.leq X_0 (fp #b0 #x7f #b00000000000000000000000)))
(assert (fp.geq X_0 (_ +zero 8 24)))
(assert (fp.leq X_1 (fp #b0 #x7f #b00000000000000000000000)))
(assert (fp.geq X_1 (_ +zero 8 24)))
(declare-fun H_0_0 () (_ FloatingPoint 8 24))
(declare-fun H_0_1 () (_ FloatingPoint 8 24))
(declare-fun H_0_2 () (_ FloatingPoint 8 24))
(declare-fun H_0_3 () (_ FloatingPoint 8 24))
(declare-fun H_0_4 () (_ FloatingPoint 8 24))
(declare-fun H_0_5 () (_ FloatingPoint 8 24))
(declare-fun H_0_6 () (_ FloatingPoint 8 24))
(assert (= H_0_0 (fp.add roundNearestTiesToEven
        (fp.add roundNearestTiesToEven
                (fp #b0 #x7f #b00000000000000000000000)
                (fp.mul roundNearestTiesToEven
                        (fp #b1 #x7f #b00000000000000000000000)
                        X_0))
        (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_1))))
(assert (= H_0_1 (fp.add roundNearestTiesToEven
        (fp.add roundNearestTiesToEven
                (_ +zero 8 24)
                (fp.mul roundNearestTiesToEven
                        (fp #b0 #x7f #b00000000000000000000000)
                        X_0))
        (fp.mul roundNearestTiesToEven
                (fp #b1 #x7f #b00000000000000000000000)
                X_1))))
(assert (= H_0_2 (fp.add roundNearestTiesToEven
        (fp.add roundNearestTiesToEven
                (fp #b1 #x7f #b00000000000000000000000)
                (fp.mul roundNearestTiesToEven
                        (fp #b0 #x7f #b00000000000000000000000)
                        X_0))
        (fp.mul roundNearestTiesToEven
                (fp #b0 #x7f #b00000000000000000000000)
                X_1))))
(assert (= H_0_3 (fp.add roundNearestTiesToEven
        (fp.add roundNearestTiesToEven
                (_ +zero 8 24)
                (fp.mul roundNearestTiesToEven
                        (fp #b0 #x7f #b00000000000000000000000)
                        X_0))
        (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_1))))
(assert (= H_0_4 (fp.add roundNearestTiesToEven
        (fp.add roundNearestTiesToEven
                (_ +zero 8 24)
                (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_0))
        (fp.mul roundNearestTiesToEven
                (fp #b0 #x7f #b00000000000000000000000)
                X_1))))
(assert (= H_0_5 (fp.add roundNearestTiesToEven
        (fp.add roundNearestTiesToEven
                (fp #b1 #x7f #b00000000000000000000000)
                (fp.mul roundNearestTiesToEven
                        (fp #b0 #x80 #b00000000000000000000000)
                        X_0))
        (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_1))))
(assert (= H_0_6 (fp.add roundNearestTiesToEven
        (fp.add roundNearestTiesToEven
                (fp #b1 #x7f #b00000000000000000000000)
                (fp.mul roundNearestTiesToEven (_ +zero 8 24) X_0))
        (fp.mul roundNearestTiesToEven
                (fp #b0 #x80 #b00000000000000000000000)
                X_1))))
(declare-fun H_1_0 () (_ FloatingPoint 8 24))
(declare-fun H_1_1 () (_ FloatingPoint 8 24))
(declare-fun H_1_2 () (_ FloatingPoint 8 24))
(declare-fun H_1_3 () (_ FloatingPoint 8 24))
(declare-fun H_1_4 () (_ FloatingPoint 8 24))
(declare-fun H_1_5 () (_ FloatingPoint 8 24))
(declare-fun H_1_6 () (_ FloatingPoint 8 24))
(assert (= H_1_0 (ite (fp.geq H_0_0 (_ +zero 8 24)) H_0_0 (_ +zero 8 24))))
(assert (= H_1_1 (ite (fp.geq H_0_1 (_ +zero 8 24)) H_0_1 (_ +zero 8 24))))
(assert (= H_1_2 (ite (fp.geq H_0_2 (_ +zero 8 24)) H_0_2 (_ +zero 8 24))))
(assert (= H_1_3 (ite (fp.geq H_0_3 (_ +zero 8 24)) H_0_3 (_ +zero 8 24))))
(assert (= H_1_4 (ite (fp.geq H_0_4 (_ +zero 8 24)) H_0_4 (_ +zero 8 24))))
(assert (= H_1_5 (ite (fp.geq H_0_5 (_ +zero 8 24)) H_0_5 (_ +zero 8 24))))
(assert (= H_1_6 (ite (fp.geq H_0_6 (_ +zero 8 24)) H_0_6 (_ +zero 8 24))))
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
                                           (_ +zero 8 24)
                                           H_1_3))
                           (fp.mul roundNearestTiesToEven (_ +zero 8 24) H_1_4))
                   (fp.mul roundNearestTiesToEven (_ +zero 8 24) H_1_5))))
  (fp.add roundNearestTiesToEven
          a!2
          (fp.mul roundNearestTiesToEven (_ +zero 8 24) H_1_6))))))
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
                                           (fp #b0 #x7f #b00000000000000000000000)
                                           H_1_3))
                           (fp.mul roundNearestTiesToEven
                                   (fp #b0 #x7f #b00000000000000000000000)
                                   H_1_4))
                   (fp.mul roundNearestTiesToEven
                           (fp #b1 #x7f #b00000000000000000000000)
                           H_1_5))))
  (fp.add roundNearestTiesToEven
          a!2
          (fp.mul roundNearestTiesToEven
                  (fp #b1 #x7f #b00000000000000000000000)
                  H_1_6))))))
(declare-fun Y_0 () (_ FloatingPoint 8 24))
(assert (= Y_0 H_2_0))
(declare-fun Y_1 () (_ FloatingPoint 8 24))
(assert (= Y_1 H_2_1))
(assert (fp.geq Y_0 (fp #b0 #x7f #b00000000000000000000000)))
(assert (fp.leq Y_1 (_ +zero 8 24)))
(check-sat)
(get-model)