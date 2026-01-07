/* -*- c++ -*- */
/*
 * Copyright 2026 yulong.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_RFID_GATE_H
#define INCLUDED_RFID_GATE_H

#include <gnuradio/rfid/api.h>
#include <gnuradio/block.h>

namespace gr {
  namespace rfid {

    /*!
     * \brief <+description of block+>
     * \ingroup rfid
     *
     */
    class RFID_API gate : virtual public gr::block
    {
     public:
      typedef std::shared_ptr<gate> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of rfid::gate.
       *
       * To avoid accidental use of raw pointers, rfid::gate's
       * constructor is in a private implementation
       * class. rfid::gate::make is the public interface for
       * creating new instances.
       */
      static sptr make(int sample_rate);
    };

  } // namespace rfid
} // namespace gr

#endif /* INCLUDED_RFID_GATE_H */
