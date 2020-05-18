import {
  get_puzzle_hash,
  format_message,
  incomingMessage,
  get_balance_for_wallet,
  get_transactions,
  get_height_info,
  get_sync_status,
  get_connection_info,
  get_colour_info,
  get_colour_name,
  pingWallet
} from "../modules/message";

import { createState } from "../modules/createWalletReducer";
import { offerParsed, resetTrades } from "../modules/TradeReducer";
import { openDialog } from "../modules/dialogReducer";
import {
  service_wallet_server,
  service_full_node,
  service_simulator,
  service_farmer,
  service_harvester
} from "../util/service_names";
import {
  pingFullNode,
  getBlockChainState,
  getLatestBlocks,
  getFullNodeConnections,
} from "../modules/fullnodeMessages";
import {
  getLatestChallenges,
  getFarmerConnections,
  pingFarmer
} from "../modules/farmerMessages";
import { getPlots, pingHarvester } from "../modules/harvesterMessages";
import {
  changeEntranceMenu,
  presentSelectKeys,
  presentNewWallet
} from "../modules/entranceMenu";

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function ping_wallet(store) {
  console.log("pining wallet");
  await sleep(1500);
  store.dispatch(pingWallet());
}

async function ping_full_node(store) {
  console.log("pining ful node");
  await sleep(1500);
  store.dispatch(pingFullNode());
}

async function ping_farmer(store) {
  console.log("pining farmer");
  await sleep(1500);
  store.dispatch(pingFarmer());
}

async function ping_harvester(store) {
  console.log("pining harvester");
  await sleep(1500);
  store.dispatch(pingHarvester());
}

export const handle_message = (store, payload) => {
  store.dispatch(incomingMessage(payload));
  if (payload.command === "ping") {
    if (payload.origin === service_wallet_server) {
      console.log("Got ping from wallet");
      store.dispatch(format_message("get_public_keys", {}));
      store.dispatch(format_message("get_wallets", {}));
      store.dispatch(get_height_info());
      store.dispatch(get_sync_status());
      store.dispatch(get_connection_info());
    } else if (payload.origin === service_full_node) {
      store.dispatch(getBlockChainState());
      store.dispatch(getLatestBlocks());
      store.dispatch(getFullNodeConnections());
    } else if (payload.origin === service_farmer) {
      store.dispatch(getLatestChallenges());
      store.dispatch(getFarmerConnections());
    } else if (payload.origin === service_harvester) {
      store.dispatch(getPlots());
    }
  } else if (payload.command === "log_in") {
    if (payload.data.success) {
      store.dispatch(format_message("get_wallets", {}));
    }
  } else if (payload.command === "logged_in") {
    if (payload.data.logged_in) {
      store.dispatch(format_message("get_wallets", {}));
    }
  }
  if (payload.command === "add_key") {
    if (payload.data.success) {
      store.dispatch(format_message("get_wallets", {}));
      store.dispatch(format_message("get_public_keys", {}));
    }
  } else if (payload.command === "delete_key") {
    if (payload.data.success) {
      store.dispatch(format_message("get_public_keys", {}));
    }
  } else if (payload.command === "delete_all_keys") {
    if (payload.data.success) {
      store.dispatch(format_message("get_public_keys", {}));
    }
  } else if (payload.command === "get_public_keys") {
    if (
      payload.data.success &&
      payload.data.public_key_fingerprints.length > 0
    ) {
      store.dispatch(changeEntranceMenu(presentSelectKeys));
    } else {
      store.dispatch(changeEntranceMenu(presentNewWallet));
    }
  } else if (
    payload.command === "close_connection" ||
    payload.command === "open_connection"
  ) {
    if (payload.origin === service_farmer) {
      store.dispatch(getFarmerConnections());
    }
  } else if (payload.command === "delete_plot") {
    store.dispatch(getPlots());
  } else if (payload.command === "get_wallets") {
    if (payload.data.success) {
      const wallets = payload.data.wallets;
      for (let wallet of wallets) {
        store.dispatch(get_balance_for_wallet(wallet.id));
        store.dispatch(get_transactions(wallet.id));
        store.dispatch(get_puzzle_hash(wallet.id));
        if (wallet.type === "COLOURED_COIN") {
          store.dispatch(get_colour_name(wallet.id));
          store.dispatch(get_colour_info(wallet.id));
        }
      }
    }
  } else if (payload.command === "state_changed") {
    const state = payload.data.state;
    if (state === "coin_added" || state === "coin_removed") {
      var wallet_id = payload.data.wallet_id;
      store.dispatch(get_balance_for_wallet(wallet_id));
      store.dispatch(get_transactions(wallet_id));
    } else if (state === "sync_changed") {
      store.dispatch(get_sync_status());
    } else if (state === "new_block") {
      store.dispatch(get_height_info());
    } else if (state === "pending_transaction") {
      wallet_id = payload.data.wallet_id;
      store.dispatch(get_balance_for_wallet(wallet_id));
      store.dispatch(get_transactions(wallet_id));
    }
  } else if (payload.command === "create_new_wallet") {
    if (payload.data.success) {
      store.dispatch(format_message("get_wallets", {}));
    }
    store.dispatch(createState(true, false));
  } else if (payload.command === "cc_set_name") {
    if (payload.data.success) {
      const wallet_id = payload.data.wallet_id;
      store.dispatch(get_colour_name(wallet_id));
    }
  } else if (payload.command === "respond_to_offer") {
    if (payload.data.success) {
      store.dispatch(openDialog("Success!", "Offer accepted"));
    }
    store.dispatch(resetTrades());
  } else if (payload.command === "get_wallets") {
    if (payload.data.success) {
      const wallets = payload.data.wallets;
      // console.log(wallets);
      for (let wallet of wallets) {
        store.dispatch(get_balance_for_wallet(wallet.id));
        store.dispatch(get_transactions(wallet.id));
        store.dispatch(get_puzzle_hash(wallet.id));
        if (wallet.type === "COLOURED_COIN") {
          store.dispatch(get_colour_name(wallet.id));
          store.dispatch(get_colour_info(wallet.id));
        }
      }
    }
  } else if (payload.command === "get_discrepancies_for_offer") {
    if (payload.data.success) {
      store.dispatch(offerParsed(payload.data.discrepancies));
    }
  } else if (payload.command === "start_service") {
    const service = payload.data.service;
    if (payload.data.success) {
      if (service === service_wallet_server) {
        ping_wallet(store);
      } else if (service === service_full_node) {
        ping_full_node(store);
      } else if (service === service_simulator) {
        ping_full_node(store);
      } else if (service === service_farmer) {
        ping_farmer(store);
      } else if (service === service_harvester) {
        ping_harvester(store);
      }
    } else if (payload.data.error === "already running") {
      if (service === service_wallet_server) {
        ping_wallet(store);
      } else if (service === service_full_node) {
        ping_full_node(store);
      } else if (service === service_simulator) {
        ping_full_node(store);
      } else if (service === service_farmer) {
        ping_farmer(store);
      } else if (service === service_harvester) {
        ping_harvester(store);
      }
    }
  }
  if (payload.data.success === false) {
    if (payload.data.reason) {
      store.dispatch(openDialog("Error?", payload.data.reason));
    }
  }
};
