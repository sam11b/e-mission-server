import sys
import logging
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',
    level=logging.DEBUG)

import emission.net.usercache.abstract_usercache_handler as euah
import emission.net.usercache.abstract_usercache as enua
import emission.storage.timeseries.abstract_timeseries as esta

import emission.analysis.intake.cleaning.filter_accuracy as eaicf
import emission.analysis.intake.segmentation.trip_segmentation as eaist
import emission.analysis.intake.segmentation.section_segmentation as eaiss
import emission.analysis.intake.cleaning.location_smoothing as eaicl

if __name__ == '__main__':
    cache_uuid_list = enua.UserCache.get_uuid_list()
    logging.info("cache UUID list = %s" % cache_uuid_list)

    for uuid in cache_uuid_list:
        logging.info("*" * 10 + "UUID %s: moving to long term" % uuid + "*" * 10)
        uh = euah.UserCacheHandler.getUserCacheHandler(uuid)
        uh.moveToLongTerm()

    long_term_uuid_list = esta.TimeSeries.get_uuid_list()
    logging.info("*" * 10 + "long term UUID list = %s" % long_term_uuid_list)
    for uuid in long_term_uuid_list:
        logging.info("*" * 10 + "UUID %s: filter accuracy if needed" % uuid + "*" * 10)
        eaicf.filter_accuracy(uuid)
        
        logging.info("*" * 10 + "UUID %s: segmenting into trips" % uuid + "*" * 10)
        eaist.segment_current_trips(uuid)

        logging.info("*" * 10 + "UUID %s: segmenting into sections" % uuid + "*" * 10)
        eaiss.segment_current_sections(uuid)

        logging.info("*" * 10 + "UUID %s: smoothing sections" % uuid + "*" * 10)
        eaicl.filter_current_sections(uuid)

        logging.info("*" * 10 + "UUID %s: storing views to cache" % uuid + "*" * 10)
        uh = euah.UserCacheHandler.getUserCacheHandler(uuid)
        uh.storeViewsToCache()
